import sublime, sublime_plugin
import os
import os.path
import time
import sys


class EnjoyCommand(sublime_plugin.TextCommand):
	def run(self, edit,**args):
		def on_cancel():
			return

		def on_change(name):
			return

		def GetParentPath(strPath):  
		  if not strPath:  
		      return None;  
		    
		  lsPath = os.path.split(strPath);  
		  if lsPath[1]:  
		      return lsPath[0];  
		    
		  lsPath = os.path.split(lsPath[0]);  
		  return lsPath[0]; 

		def checkenjoy(path):
			if  os.path.exists(path+"/enjoy.json"):
				return path;
			else:
				return checkenjoy(GetParentPath(path))

		def on_done(name):
			# for key, value in self.view.window().extract_variables().items():
			# 	print(key,value)
			# platform Windows
			# file_extension html
			# file_name index.html
			# folder D:\wamp\www\360
			# file_path C:\Users\colacao.CAOYUE\Desktop\Test\src\home
			# file C:\Users\colacao.CAOYUE\Desktop\Test\src\home\index.html
			# file_base_name index
			# packages C:\Users\colacao.CAOYUE\AppData\Roaming\Sublime Text 3\Packages
			dirs = self.view.window().extract_variables()['file_path']
			enjoy = checkenjoy(dirs)
			# if enjoy:
			# 	sublime.message_dialog("找到enjoy目录"+enjoy)

			sublime.message_dialog("当前文件=="+dirs+"\n"+"用户输入=="+name+"\n"+"enjoy目录=="+checkenjoy(dirs)+"\n"+"命令参数=="+args['id'])
		 

		print(args['id'])
		self.view.window().show_input_panel('请输入项目名称','Test',on_done,on_change,on_cancel)

