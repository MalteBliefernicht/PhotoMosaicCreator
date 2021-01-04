import wx
import numpy as np
from PIL import Image
import os
import math
from time import sleep
import pickle



class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
        
    def OnDropFiles(self, x, y, filenames):
        self.window.SetInsertionPointEnd()
        
        for name in filenames:
            self.window.update_text(os.path.split(name)[1] + '\n')
            self.window.picture_list.append(name)


class Notebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, size=(300,350), style=0)
        
        self.tab_one = wx.Panel(self)
        self.AddPage(self.tab_one, 'PhotoMosaic')
        
        self.tab_two = wx.Panel(self)
        self.AddPage(self.tab_two, 'ImageCropper')
        
        self.input_picture_path = self.load_path()
        self.source_folder_path = self.load_path2()
        self.save_location_path = ''
        file_drop_target = FileDrop(self)
        self.picture_list = []
        self.save_location2 = ''

        rows = wx.BoxSizer(wx.VERTICAL)
        
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        text1 = wx.StaticText(self.tab_one, label='Choose Input Picture')
        row1.Add(text1, flag=wx.RIGHT | wx.TOP |wx.LEFT, border=10)
        rows.Add(row1)
        
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        self.text_ctrl2 = wx.TextCtrl(self.tab_one)
        self.text_ctrl2.SetValue(self.input_picture_path)
        row2.Add(self.text_ctrl2, flag=wx.RIGHT |wx.LEFT, border=10)
        button2 = wx.Button(self.tab_one, label='Browse')
        button2.Bind(wx.EVT_BUTTON, self.input_picture)
        row2.Add(button2, flag=wx.RIGHT |wx.LEFT, border=10)
        rows.Add(row2)
        
        row_empty = wx.BoxSizer(wx.HORIZONTAL)
        text_empty = wx.StaticText(self.tab_one, label='')
        row_empty.Add(text_empty)
        rows.Add(row_empty, flag=wx.RIGHT | wx.TOP |wx.LEFT, border=5)
        
        row3 = wx.BoxSizer(wx.HORIZONTAL)
        text3 = wx.StaticText(self.tab_one, label='Choose Source Folder')
        row3.Add(text3, flag=wx.RIGHT | wx.TOP |wx.LEFT, border=10)
        rows.Add(row3)
        
        row4 = wx.BoxSizer(wx.HORIZONTAL)
        self.text_ctrl4 = wx.TextCtrl(self.tab_one)
        self.text_ctrl4.SetValue(self.source_folder_path)
        row4.Add(self.text_ctrl4, flag=wx.RIGHT |wx.LEFT, border=10)
        button4 = wx.Button(self.tab_one, label='Browse')
        button4.Bind(wx.EVT_BUTTON, self.source_folder)
        row4.Add(button4, flag=wx.RIGHT |wx.LEFT, border=10)
        rows.Add(row4)
        
        row_empty2 = wx.BoxSizer(wx.HORIZONTAL)
        text_empty2 = wx.StaticText(self.tab_one, label='')
        row_empty2.Add(text_empty2)
        rows.Add(row_empty2, flag=wx.RIGHT | wx.TOP |wx.LEFT, border=5)

        row7 = wx.BoxSizer(wx.HORIZONTAL)
        text7 = wx.StaticText(self.tab_one, label='Segment Size')
        row7.Add(text7, flag=wx.RIGHT | wx.TOP |wx.LEFT, border=10)
        rows.Add(row7)
        
        row8 = wx.BoxSizer(wx.HORIZONTAL)
        self.text_ctrl8 = wx.TextCtrl(self.tab_one)
        self.text_ctrl8.SetValue('10')
        row8.Add(self.text_ctrl8, flag=wx.RIGHT |wx.LEFT, border=10)
        rows.Add(row8)
        
        row9 = wx.BoxSizer(wx.HORIZONTAL)
        button9 = wx.Button(self.tab_one, label='Create Mosaic')
        button9.Bind(wx.EVT_BUTTON, self.create_mosaic)
        row9.Add(button9, flag=wx.RIGHT | wx.TOP |wx.LEFT, border=30)
        rows.Add(row9, flag=wx.CENTER)
        
        self.tab_one.SetSizer(rows)

        main_sizer = wx.BoxSizer(wx.VERTICAL)        
        
        sizer10 = wx.BoxSizer(wx.HORIZONTAL)
        self.text10 = wx.StaticText(self.tab_two, label='Drop Files In The Box')
        sizer10.Add(self.text10)
        main_sizer.Add(sizer10, flag=wx.LEFT | wx.TOP, border=10)
        
        sizer20 = wx.BoxSizer(wx.HORIZONTAL)
        self.drop_box = wx.TextCtrl(self.tab_two, style=wx.TE_MULTILINE | wx.TE_READONLY)
        sizer20.Add(self.drop_box, proportion=1, flag=wx.EXPAND)
        main_sizer.Add(sizer20, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)

        sizer30 = wx.BoxSizer(wx.HORIZONTAL)
        button30 = wx.Button(self.tab_two, label='Clear List')
        button30.Bind(wx.EVT_BUTTON, self.clear_button)
        sizer30.Add(button30)
        main_sizer.Add(sizer30, flag=wx.LEFT | wx.TOP, border=10)

        sizer40 = wx.BoxSizer(wx.HORIZONTAL)
        text40 = wx.StaticText(self.tab_two, label='Destination')
        sizer40.Add(text40)
        main_sizer.Add(sizer40, flag=wx.LEFT | wx.TOP, border=10)
        
        sizer50 = wx.BoxSizer(wx.HORIZONTAL)
        self.box50 = wx.TextCtrl(self.tab_two)
        sizer50.Add(self.box50, flag=wx.RIGHT, border=10)
        button50 = wx.Button(self.tab_two, label='Browse')
        button50.Bind(wx.EVT_BUTTON, self.browse_button)
        sizer50.Add(button50)
        main_sizer.Add(sizer50, flag=wx.LEFT, border=10)
        
        sizer60 = wx.BoxSizer(wx.HORIZONTAL)
        text60 = wx.StaticText(self.tab_two, label='Size in Pixel')
        sizer60.Add(text60)
        main_sizer.Add(sizer60, flag=wx.LEFT | wx.TOP, border=10)
        
        sizer70 = wx.BoxSizer(wx.HORIZONTAL)
        self.box70 = wx.TextCtrl(self.tab_two)
        sizer70.Add(self.box70)
        main_sizer.Add(sizer70, flag=wx.LEFT, border=10)        
        
        sizer80 = wx.BoxSizer(wx.HORIZONTAL)
        button80 = wx.Button(self.tab_two, label='Start')
        sizer80.Add(button80)
        button80.Bind(wx.EVT_BUTTON, self.button_press)
        main_sizer.Add(sizer80, proportion=1, flag=wx.CENTRE | wx.TOP, border=25)
        
        self.drop_box.SetDropTarget(file_drop_target)
        self.tab_two.SetSizer(main_sizer)
        
    def input_picture(self, event):
        title = "Choose a picture:"
        dialog = wx.FileDialog(self, title, defaultDir=os.path.split(self.input_picture_path)[0],
            style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.input_picture_path = dialog.GetPath()
        dialog.Destroy()
        self.text_ctrl2.SetValue(self.input_picture_path)

    def source_folder(self, event):
        title = "Choose a folder:"
        dialog = wx.DirDialog(self, title, defaultPath=self.source_folder_path, style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.source_folder_path = dialog.GetPath()
        dialog.Destroy()
        self.text_ctrl4.SetValue(self.source_folder_path)

    def save_location(self):
        title = "Choose a folder:"
        dialog = wx.FileDialog(self, title, wildcard="*.jpg",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            self.save_location_path = dialog.GetPath()
            self.im_new.save(self.save_location_path)
        dialog.Destroy()
        
    def save_question(self):
        message = "Do you want to save this picture?"
        dialog = wx.MessageDialog(self, message,
            style=wx.YES_NO | wx.STAY_ON_TOP | wx.CENTRE)
        if dialog.ShowModal() == wx.ID_YES:
            self.save_location()
        dialog.Destroy()
            
    def segment_sizes(self):
        var = self.text_ctrl8.GetValue()
        return var

    def save_path(self, path):
        try:
            file_object = open(os.getcwd()+r'\pathdata.pydata', 'wb')
            pickle.dump(path, file_object)
            file_object.close()
            
        except Exception as e:
            print(e)
                   
    def save_path2(self, path):
        try:
            file_object = open(os.getcwd()+r'\pathdata2.pydata', 'wb')
            pickle.dump(path, file_object)
            file_object.close()
            
        except Exception as e:
            print(e)            
            
    def load_path(self):
        try:
            file_object = open(os.getcwd()+r'\pathdata.pydata', 'rb')
            path = pickle.load(file_object)
            file_object.close()  
            return path
        
        except Exception as e:
            print(e)
            return os.getcwd()            
            
    def load_path2(self):
        try:
            file_object = open(os.getcwd()+r'\pathdata2.pydata', 'rb')
            path = pickle.load(file_object)
            file_object.close()
            return path
            
        except Exception as e:
            print(e)
            return os.getcwd()

    def create_mosaic(self, event):
        im = Image.open(self.input_picture_path)
        im_size = im.size
        r, g, b = im.split()

        segment_size = int(self.segment_sizes())
        r_list = []
        g_list = []
        b_list = []
        r_array = np.array(r)
        g_array = np.array(g)
        b_array = np.array(b)
        average_r = []
        average_g = []
        average_b = []
        combined_average = []
        combined_average_source = {}
        source_images = []
        self.im_new = Image.new(mode = 'RGB', size = (im_size))

        for r in range(0, im_size[1], segment_size):
            for c in range(0, im_size[0], segment_size):
                arr_slice = r_array[0+r:segment_size+r, 0+c:segment_size+c]
                r_list.append(arr_slice)

        for r in range(0, im_size[1], segment_size):
            for c in range(0, im_size[0], segment_size):
                arr_slice = g_array[0+r:segment_size+r, 0+c:segment_size+c]
                g_list.append(arr_slice)

        for r in range(0, im_size[1], segment_size):
            for c in range(0, im_size[0], segment_size):
                arr_slice = b_array[0+r:segment_size+r, 0+c:segment_size+c]
                b_list.append(arr_slice)

        for x in r_list:
            temp_list = []
            for single in x:        
                step1 = sum(single) / len(single)
                temp_list.append(step1)
            temp_result = sum(temp_list) / len(temp_list)
            average_r.append(temp_result)

        for x in g_list:
            temp_list = []
            for single in x:        
                step1 = sum(single) / len(single)
                temp_list.append(step1)
            temp_result = sum(temp_list) / len(temp_list)
            average_g.append(temp_result)

        for x in b_list:
            temp_list = []
            for single in x:        
                step1 = sum(single) / len(single)
                temp_list.append(step1)
            temp_result = sum(temp_list) / len(temp_list)
            average_b.append(temp_result)

        for index, red in enumerate(average_r):
            rgb_tuple = (average_r[index], average_g[index], average_b[index])
            combined_average.append(rgb_tuple)

        in_path = self.source_folder_path

        for image_path in os.listdir(in_path):
            input_path = os.path.join(in_path, image_path)
            
            im_source = Image.open(input_path)
            r_source, g_source, b_source = im_source.split()
            
            r_array_source = np.array(r_source)
            g_array_source = np.array(g_source)
            b_array_source = np.array(b_source)
            
            r_list_source = []
            g_list_source = []
            b_list_source = []
            
            for row in r_array_source:
                for number in row:
                    r_list_source.append(number)
            
            for row in g_array_source:
                for number in row:
                    g_list_source.append(number)
            
            for row in b_array_source:
                for number in row:
                    b_list_source.append(number)
                    
            average_r_source = sum(r_list_source) / len(r_list_source)
            average_g_source = sum(g_list_source) / len(g_list_source)
            average_b_source = sum(b_list_source) / len(b_list_source)            
            
            rgb_tuple_source = (average_r_source, average_g_source, average_b_source)
            combined_average_source[image_path] = rgb_tuple_source                

        for segment in combined_average:
            distance_list = {}
            for key, value in combined_average_source.items():
                distance = math.sqrt((value[0]-segment[0])**2+(value[1]-segment[1])**2+(value[2]-segment[2])**2)
                distance_list[key] = math.floor(distance)                                
                
            min_distance = min(distance_list.keys(), key=(lambda k: distance_list[k]))
            source_images.append(min_distance)
            
        index = 0        
        for r in range(0, im_size[1], segment_size):
            for c in range(0, im_size[0], segment_size):
                in_path = self.source_folder_path
                input_path = os.path.join(in_path, source_images[index])
                segment = Image.open(input_path)
                region = segment.resize((segment_size, segment_size))
                index = index + 1
                box = (0+c, 0+r, segment_size+c, segment_size+r)
                self.im_new.paste(region, box)

        self.im_new.show()
        sleep(1)
        self.save_question()
        self.save_path(self.input_picture_path)
        self.save_path2(self.source_folder_path)        
        
    def SetInsertionPointEnd(self):
        self.drop_box.SetInsertionPointEnd()
        
    def update_text(self, text):
        self.drop_box.WriteText(text)
    
    def button_press(self, event):
        out_path = self.save_location2
        segment_size = int(self.segment_sizer())

        for image_path in self.picture_list:
            im = Image.open(image_path)
            im_size = min(im.size)
            box = (0, 0, im_size, im_size)
            region = im.crop(box)
            result = region.resize((segment_size, segment_size))
            
            fulloutpath = os.path.join("%s\%s" % (out_path, os.path.basename(image_path)))
            result.save(fulloutpath)
        
        wx.MessageBox('All pictures have been cropped.', 'Complete', wx.OK)
    
    def clear_button(self, event):
        for number in range(0, len(self.picture_list)):
            del self.picture_list[0]
        self.drop_box.Clear()
        
    def browse_button(self, event):
        title = 'Select Save Folder'
        dialog = wx.DirDialog(self, title, style=wx.DD_DEFAULT_STYLE)
        if dialog.ShowModal() == wx.ID_OK:
            self.save_location2 = dialog.GetPath()
        dialog.Destroy()
        self.box50.SetValue(self.save_location2)
    
    def segment_sizer(self):
        var = self.box70.GetValue()
        return var
  
 
class PhotoFrame(wx.Frame):
    def __init__(self):
        super(PhotoFrame, self).__init__(parent=None, title='Photomosaic Creator', size=(300,350))
        self.Centre()
        panel = wx.Panel(self)
        notebook = Notebook(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, flag=wx.ALL|wx.EXPAND)
        panel.SetSizer(sizer)

        self.Show()
 
 
        
if __name__ == '__main__':
    app = wx.App()
    frame = PhotoFrame()
    app.MainLoop()
