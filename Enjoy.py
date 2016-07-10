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
			desktop =  os.path.expanduser('~')	+"\Desktop"	
			os.system("cd "+desktop+" "+" && "+"enjoy init " + name)
			
		 


		dirs = self.view.window().extract_variables()

		
		if (args['id']=="init"):
			self.view.window().show_input_panel('请输入项目名称','Test',on_done,on_change,on_cancel)

		if "file_path" in dirs:	
			dir1 = dirs['file_path']
			enjoy = checkenjoy(dir1)
			if(enjoy and args['id']=="start"):
				os.system("cd "+enjoy+"/rn"+" && "+"react-native start")

			if(enjoy and  args['id']=="build" and not args['value']=="h5"):
				os.system("cd "+enjoy+""+" && "+"enjoy build --rn")

			if(enjoy and args['id']=="build" and args['value']=="h5"):
				print("cd "+enjoy+""+" && "+"enjoy build --web && cd web && webpack")
				os.system("cd "+enjoy+""+" && "+"enjoy build --web && cd web && webpack")

			if(enjoy and  args['id']=="run"):
				print("cd "+enjoy+""+" && "+"enjoy run --"+args['value'])
				os.system("cd "+enjoy+""+" && "+"enjoy run --"+args['value'])
		else:
			if (not args['id']=="init"):
				sublime.message_dialog("当前文件不属于enjoy项目")