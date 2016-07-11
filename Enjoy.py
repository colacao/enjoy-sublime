import sublime, sublime_plugin
import os
import os.path
import time
import sys
import subprocess
from . import SublimeHelper as SH
from . import OsShell
class EnjoyCommand(sublime_plugin.TextCommand):
	def __init__(self,num):
		print('HelloEnjoy')

	def get_view_and_window(self, view=None):
	  if view is None:
	      view = self.view

	  if view is not None:
	      window = view.window()

	  # But if the view doesn't have a window, or there is no view at
	  # all, then use the active window and view as set in the Sublime
	  # module:
	  #
	  if view is None or window is None:
	      window = sublime.active_window()
	      view = window.active_view()

	  return view, window

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
				spath = GetParentPath(path);
				if not spath=="/":
					return checkenjoy(spath)
				else:
					return ""

		def on_done(name):
			print(self.rn)
			print(self.enjoy)
			desktop =  os.path.expanduser('~')	+"/Desktop"	
			print("cd "+desktop+" "+" && "+"enjoy init " + name)
			self.progress = SH.ProgressDisplay(self.view, "Enjoy", "创建中...", 250)
			self.progress.start()
			def _C2(output):
				print(output)
				if output is None:
					self.progress.stop()

			OsShell.process("cd "+desktop+" "+" && "+"/Users/user/.node/bin/enjoy init " + name,_C2)
		 


		dirs = self.view.window().extract_variables()

		
		if (args['id']=="init"):
			self.view.window().show_input_panel('请输入项目名称','Test',on_done,on_change,on_cancel)

		if "file_path" in dirs:	
			dir1 = dirs['file_path']
			enjoy = checkenjoy(dir1)
			if(enjoy and args['id']=="start"):
				print("cd "+enjoy+"/rn"+" && "+"react-native start")
				self.progress = SH.ProgressDisplay(self.view, "Enjoy", "服务启动中...", 250)
				self.progress.start()
				def _C2(output):
					print(output)
					if output is None:
						self.progress.stop()

				OsShell.process("cd "+enjoy+"/rn"+" && "+"/Users/user/.node/bin/react-native start",_C2)


			if(enjoy and  args['id']=="build" and not args['value']=="h5"):
				self.progress = SH.ProgressDisplay(self.view, "Enjoy", "编译中...", 250)
				self.progress.start()
				def _C2(output):
					if output is None:
						self.progress.stop()

				OsShell.process("cd "+enjoy+""+" && "+"/Users/user/.node/bin/enjoy build --rn",_C2)


			if(enjoy and args['id']=="build" and args['value']=="h5"):
				print("cd "+enjoy+""+" && "+"enjoy build --web && cd web && webpack")
				# abc = os.popen("cd "+enjoy+""+" && "+"enjoy build --web && cd web && webpack")
				self.progress = SH.ProgressDisplay(self.view, "Enjoy", "创建中...", 250)
				self.progress.start()
				def _C2(output):
					print(output)
					if output is None:
						self.progress.stop()

				OsShell.process("cd "+enjoy+""+" && "+"/Users/user/.node/bin/enjoy build --web && cd web && webpack",_C2)

			if(enjoy and  args['id']=="run"):
				print("cd "+enjoy+""+" && "+"enjoy run --"+args['value'])
				# os.system("cd "+enjoy+""+" && "+"enjoy run --"+args['value'])
				self.progress = SH.ProgressDisplay(self.view, "Enjoy", "创建中...", 250)
				self.progress.start()
				def _C2(output):
					print(output)
					if output is None:
						self.progress.stop()

				OsShell.process("cd "+enjoy+""+" && "+"/Users/user/.node/bin/enjoy run --"+args['value'],_C2)
		 
		else:
			if (not args['id']=="init"):
				sublime.message_dialog("当前文件不属于enjoy项目")

