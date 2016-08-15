import sublime, sublime_plugin
import os
import os.path
import time
import sys
import webbrowser
import subprocess
import  shutil
import threading, time
import re
from . import SublimeHelper as SH
from . import OsShell
global Pref, s, Cache
Pref = {}
s = {}
class EnjoyCommand(sublime_plugin.TextCommand):
	def get_settings(self):
		settings = self.view.settings().get('Enjoy')
		if settings is None:
			settings = sublime.load_settings('Enjoy.sublime-settings')
		return settings



	def get_view_and_window(self, view=None):
	  if view is None:
	      view = self.view

	  if view is not None:
	      window = view.window()

	  if view is None or window is None:
	      window = sublime.active_window()
	      view = window.active_view()

	  return view, window

	def run(self, edit,**args):
		self.rn = self.get_settings().get('rn-path')
		self.enjoy = self.get_settings().get('enjoy-path')

		def win_browser_open(url):
			if url.startswith('file:///'):
				browser = _winreg.QueryValue(_winreg.HKEY_CLASSES_ROOT, r'http\shell\open\command')
				browser = browser.replace('%1', url)
				subprocess.Popen(shlex.split(browser))
			else:
				webbrowser.open(url)

		def normalizePath(self, fileToOpen):
				fileToOpen = fileToOpen.replace("\\", "/")
				fileToOpen = "file:///%s" % fileToOpen.replace(" ", "%20").replace("(", "%28").replace(")", "%29")

				return fileToOpen

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
			print("cd "+desktop+" "+" && "+"enjoy init " + name )
			self.progress = SH.ProgressDisplay(self.view, "Enjoy", "创建中...", 250)
			self.progress.start()
			def _C2(output):
				print(output)
				if output is None:
					self.progress.stop()
					print("open -an /Applications/Sublime\ Text.app/ ~/Desktop/"+name);
					os.system("open -a /Applications/Sublime\ Text.app/ ~/Desktop/"+name)
					print("cd "+desktop+"/"+name+"/rn && npm update ")
					def _C9(output1):
						print(output1)
						self.progress = SH.ProgressDisplay(self.view, "Enjoy", "安装依赖...", 250)
						self.progress.start()
						if output1 is None:
							self.progress.stop()
							sublime.message_dialog("项目"+name+"准备就绪,开始你的enjoy之旅")


					OsShell.process("cd "+desktop+"/"+name+"/rn && npm update ",_C9)

			print("---------------cd "+desktop+" "+" && "+self.enjoy+" init " + name)
			OsShell.process("cd "+desktop+" "+" && "+self.enjoy+" init " + name,_C2)
		 

		LOCAL = '/usr/local/bin:/usr/local/sbin:~/.node/bin'
		os.environ['PATH'] += ':'
		os.environ['PATH'] += LOCAL
		dirs = self.view.window().extract_variables()
		self.view = self.get_view_and_window()[0]
		
		if (args['id']=="init"):
			self.view.window().show_input_panel('请输入项目名称','Test',on_done,on_change,on_cancel)

		if "file_path" in dirs:	
			dir1 = dirs['file_path']
			enjoy = checkenjoy(dir1)
			if(enjoy and args['id']=="start"):
				print("cd "+enjoy+"/rn"+" && "+self.rn+" start")
				self.progress = SH.ProgressDisplay(self.view, "Enjoy", "服务启动中...", 250)
				self.progress.start()
				def _C2(output):
					print(output)
					if output is None:
						self.progress.stop()


				OsShell.process("cd "+enjoy+"/rn"+" && "+self.rn+" start",_C2)

			if(enjoy and  args['id']=="pack" and (args['value']=="ios" or args['value']=="android")):
				self.progress = SH.ProgressDisplay(self.view, "Enjoy", "打包中...", 250)
				self.progress.start()
				def _C2(output):
					print(output)
					if output is None:
						self.progress.stop()
						sublime.message_dialog("打包完成")
						print("open  "+enjoy+" /rn/"+args['value']+"/bundle/")
						OsShell.process("open  "+enjoy+"/rn/"+args['value']+"/bundle/")

				if(args['value']=="ios"):
					OsShell.process("cd "+enjoy+"/rn"+" && "+self.rn+" bundle --entry-file index.ios.js --bundle-output ./ios/bundle/index.ios.jsbundle --platform ios --assets-dest ./ios/bundle --dev false",_C2)
				else:
					OsShell.process("cd "+enjoy+"/rn"+" && "+self.rn+" bundle --entry-file index.android.js --bundle-output ./android/bundle/index.android.jsbundle --platform android --assets-dest ./android/bundle --dev false",_C2)


			if(enjoy and  args['id']=="build" and (args['value']=="ios" or args['value']=="android")):
				self.progress = SH.ProgressDisplay(self.view, "Enjoy", "编译中...", 250)
				self.progress.start()
				def _C2(output):
					print(output)
					if output is None:
						self.progress.stop()

				print("cd "+enjoy+""+" && "+self.enjoy+" build --rn")
				OsShell.process("cd "+enjoy+""+" && "+"enjoy build --rn",_C2)


			if(enjoy and args['id']=="build" and (args['value']=="h5" or args['value']=="weixin")):
				print("cd "+enjoy+""+" && "+self.enjoy+" build --web && cd web/"+args['value']+" && webpack")
				# abc = os.popen("cd "+enjoy+""+" && "+"enjoy build --web && cd web && webpack")
				self.progress = SH.ProgressDisplay(self.view, "Enjoy", "编译中...", 250)
				self.progress.start()
				def _C2(output):
					print(output)
					if output is None:
						self.progress.stop()

				OsShell.process("cd "+enjoy+""+" && "+self.enjoy+" build --web && cd web/"+args['value']+" && webpack",_C2)

			if(enjoy and  args['id']=="run" and (args['value']=="ios")):
				print("cd "+enjoy+""+" && "+self.enjoy+" build --rn")

				arr = enjoy.split('/')
				pname = arr[len(arr)-1]
				OsShell.process("open "+enjoy+"/rn/ios/"+pname+".xcodeproj/")


			if(enjoy and  args['id']=="run" and (args['value']=="h5" or args['value']=="weixin")):
				print("file://"+enjoy+"/web/"+args['value']+"/bundle/index.html")
				def _C2(output):
					print(output)
					if(output and output.find('does not exist')>=0):
						sublime.message_dialog("请先编译")
				

				if(sublime.platform() == "windows"):
					SideBarOpenInBrowserThread('','','').try_open("file://"+enjoy+"/web/"+args['value']+"/bundle/index.html","chrome")
				else:
					print("open -a Google\ Chrome 'file://"+enjoy+"/web/"+args['value']+"/bundle/index.html' --args --disable-web-security --user-data-dir")
					ret = OsShell.process("open -a Google\ Chrome 'file://"+enjoy+"/web/"+args['value']+"/bundle/index.html' --args --disable-web-security --user-data-dir",_C2)
					print(ret)

		else:
			if (not args['id']=="init"):
				sublime.message_dialog("当前文件不属于enjoy项目")




class SideBarOpenInBrowserThread(threading.Thread):
	def __init__(self, paths, type, browser):
		self.paths = paths
		self.type = type
		self.browser = browser
		threading.Thread.__init__(self)

	def run(self):
		paths = self.paths
		type = self.type
		browser = self.browser

		for item in SideBarSelection(paths).getSelectedItems():
			url = item.url(type) or item.uri()
			self.try_open(url, browser)

	def try_open(self, url, browser):
		import subprocess

		if sublime.platform() == 'windows':
			import winreg

		browser = browser.lower().strip();
		items = []

		if browser == 'chrome':
			if sublime.platform() == 'osx':
				items.extend(['open'])
				commands = ['-a', '/Applications/Google Chrome.app', url]
			elif sublime.platform() == 'windows':
				aKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
				reg_value, reg_type = winreg.QueryValueEx (aKey, "Local AppData")

				if s.get('portable_browser', '') != '':
					items.extend([s.get('portable_browser', '')])
				items.extend([
					'%HOMEPATH%\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe'

					,reg_value+'\\Chrome\\Application\\chrome.exe'
					,reg_value+'\\Google\\Chrome\\Application\\chrome.exe'
					,'%HOMEPATH%\\Google\\Chrome\\Application\\chrome.exe'
					,'%PROGRAMFILES%\\Google\\Chrome\\Application\\chrome.exe'
					,'%PROGRAMFILES(X86)%\\Google\\Chrome\\Application\\chrome.exe'
					,'%USERPROFILE%\\Local\ Settings\\Application\ Data\\Google\\Chrome\\chrome.exe'
					,'%HOMEPATH%\\Chromium\\Application\\chrome.exe'
					,'%PROGRAMFILES%\\Chromium\\Application\\chrome.exe'
					,'%PROGRAMFILES(X86)%\\Chromium\\Application\\chrome.exe'
					,'%HOMEPATH%\\Local\ Settings\\Application\ Data\\Google\\Chrome\\Application\\chrome.exe'
					,'%HOMEPATH%\\Local Settings\\Application Data\\Google\\Chrome\\Application\\chrome.exe'
					,'chrome.exe'
				])


				commands = ['-new-tab', url]
			else:
				if s.get('portable_browser', '') != '':
					items.extend([s.get('portable_browser', '')])
				items.extend([
					'/usr/bin/google-chrome'
					,'/opt/google/chrome/chrome'
					,'chrome'
					,'google-chrome'
				])
				commands = ['-new-tab', url]

		elif browser == 'canary':
			if sublime.platform() == 'osx':
					items.extend(['open'])
					commands = ['-a', '/Applications/Google Chrome Canary.app', url]
			elif sublime.platform() == 'windows':
				aKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
				reg_value, reg_type = winreg.QueryValueEx (aKey, "Local AppData")

				if s.get('portable_browser', '') != '':
					items.extend([s.get('portable_browser', '')])
				items.extend([
					'%HOMEPATH%\\AppData\\Local\\Google\\Chrome SxS\\Application\\chrome.exe'

					,reg_value+'\\Chrome SxS\\Application\\chrome.exe'
					,reg_value+'\\Google\\Chrome SxS\\Application\\chrome.exe'
					,'%HOMEPATH%\\Google\\Chrome SxS\\Application\\chrome.exe'
					,'%PROGRAMFILES%\\Google\\Chrome SxS\\Application\\chrome.exe'
					,'%PROGRAMFILES(X86)%\\Google\\Chrome SxS\\Application\\chrome.exe'
					,'%USERPROFILE%\\Local\ Settings\\Application\ Data\\Google\\Chrome SxS\\chrome.exe'
					,'%HOMEPATH%\\Local\ Settings\\Application\ Data\\Google\\Chrome SxS\\Application\\chrome.exe'
					,'%HOMEPATH%\\Local Settings\\Application Data\\Google\\Chrome SxS\\Application\\chrome.exe'
				])

				commands = ['-new-tab', url]

		elif browser == 'chromium':
			if sublime.platform() == 'osx':
				items.extend(['open'])
				commands = ['-a', '/Applications/Chromium.app', url]
			elif sublime.platform() == 'windows':
				aKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
				reg_value, reg_type = winreg.QueryValueEx (aKey, "Local AppData")
				if s.get('portable_browser', '') != '':
					items.extend([s.get('portable_browser', '')])
				items.extend([
					'%HOMEPATH%\\AppData\\Local\\Google\\Chrome SxS\\Application\\chrome.exe'

					, reg_value+'\\Chromium\\Application\\chromium.exe'
					,'%USERPROFILE%\\Local Settings\\Application Data\\Google\\Chrome\\chromium.exe'
					,'%USERPROFILE%\\Local\ Settings\\Application\ Data\\Google\\Chrome\\chromium.exe'
					,'%HOMEPATH%\\Chromium\\Application\\chromium.exe'
					,'%PROGRAMFILES%\\Chromium\\Application\\chromium.exe'
					,'%PROGRAMFILES(X86)%\\Chromium\\Application\\chromium.exe'
					,'%HOMEPATH%\\Local Settings\\Application\ Data\\Google\\Chrome\\Application\\chromium.exe'
					,'%HOMEPATH%\\Local Settings\\Application Data\\Google\\Chrome\\Application\\chromium.exe'
					,'chromium.exe'

					, reg_value+'\\Chromium\\Application\\chrome.exe'
					,'%USERPROFILE%\\Local Settings\\Application Data\\Google\\Chrome\\chrome.exe'
					,'%USERPROFILE%\\Local\ Settings\\Application\ Data\\Google\\Chrome\\chrome.exe'
					,'%HOMEPATH%\\Chromium\\Application\\chrome.exe'
					,'%PROGRAMFILES%\\Chromium\\Application\\chrome.exe'
					,'%PROGRAMFILES(X86)%\\Chromium\\Application\\chrome.exe'
					,'%HOMEPATH%\\Local\ Settings\\Application\ Data\\Google\\Chrome\\Application\\chrome.exe'
					,'%HOMEPATH%\\Local Settings\\Application Data\\Google\\Chrome\\Application\\chrome.exe'
					,'chrome.exe'

				])
				commands = ['-new-tab', url]
			else:
				if s.get('portable_browser', '') != '':
					items.extend([s.get('portable_browser', '')])
				items.extend([
					'/usr/bin/chromium'
					,'chromium'
					,'/usr/bin/chromium-browser'
					,'chromium-browser'
				])
				commands = ['-new-tab', url]
		elif browser == 'firefox':
			if sublime.platform() == 'osx':
				items.extend(['open'])
				commands = ['-a', '/Applications/Firefox.app', url]
			else:
				if s.get('portable_browser', '') != '':
					items.extend([s.get('portable_browser', '')])
				items.extend([
					'/usr/bin/firefox'

					,'%PROGRAMFILES%\\Firefox Developer Edition\\firefox.exe'
					,'%PROGRAMFILES(X86)%\\Firefox Developer Edition\\firefox.exe'

					,'%PROGRAMFILES%\\Nightly\\firefox.exe'
					,'%PROGRAMFILES(X86)%\\Nightly\\firefox.exe'

					,'%PROGRAMFILES%\\Mozilla Firefox\\firefox.exe'
					,'%PROGRAMFILES(X86)%\\Mozilla Firefox\\firefox.exe'

					,'firefox'
					,'firefox.exe'
				])
				commands = ['-new-tab', url]
		elif browser == 'opera':
			if sublime.platform() == 'osx':
				items.extend(['open'])
				commands = ['-a', '/Applications/Opera.app', url]
			else:
				if s.get('portable_browser', '') != '':
					items.extend([s.get('portable_browser', '')])
				items.extend([
					'/usr/bin/opera'
					,'/usr/bin/opera-next'
					,'/usr/bin/operamobile'

					,'%PROGRAMFILES%\\Opera\\opera.exe'
					,'%PROGRAMFILES(X86)%\\Opera\\opera.exe'

					,'%PROGRAMFILES%\\Opera\\launcher.exe'
					,'%PROGRAMFILES(X86)%\\Opera\\launcher.exe'

					,'%PROGRAMFILES%\\Opera Next\\opera.exe'
					,'%PROGRAMFILES(X86)%\\Opera Next\\opera.exe'

					,'%PROGRAMFILES%\\Opera Mobile Emulator\\OperaMobileEmu.exe'
					,'%PROGRAMFILES(X86)%\\Opera Mobile Emulator\\OperaMobileEmu.exe'

					,'opera'
					,'opera.exe'
				])
				commands = ['-newtab', url]
		elif browser == 'ie':
			if s.get('portable_browser', '') != '':
				items.extend([s.get('portable_browser', '')])
			items.extend([
				'%PROGRAMFILES%\\Internet Explorer\\iexplore.exe'
				,'%PROGRAMFILES(X86)%\\Internet Explorer\\iexplore.exe'

				,'iexplore'
				,'iexplore.exe'
			])
			commands = ['-newtab', url]
		elif browser == 'edge':
			if s.get('portable_browser', '') != '':
				items.extend([s.get('portable_browser', '')])
			items.extend(['open'])
			commands = ['-newtab', url]
		elif browser == 'safari':
			if sublime.platform() == 'osx':
				items.extend(['open'])
				commands = ['-a', 'Safari', url]
			else:
				if s.get('portable_browser', '') != '':
					items.extend([s.get('portable_browser', '')])
				items.extend([
					'/usr/bin/safari'

					,'%PROGRAMFILES%\\Safari\\Safari.exe'
					,'%PROGRAMFILES(X86)%\\Safari\\Safari.exe'

					,'Safari'
					,'Safari.exe'
				])
				commands = ['-new-tab', '-url', url]
		else:
			if s.get('portable_browser', '') != '':
				items.extend([s.get('portable_browser', '')])
			commands = ['-new-tab', url]

		for item in items:
			try:
				command2 = list(commands)
				command2.insert(0, expandVars(item))
				subprocess.Popen(command2)
				return
			except:
				try:
					command2 = list(commands)
					command2.insert(0, item)
					subprocess.Popen(command2)
					return
				except:
					pass
		try:
			if sublime.platform() == 'windows':
				if browser and browser == 'edge':
					commands = ['cmd','/c','start', 'microsoft-edge:' + url]
				else:
					commands = ['cmd','/c','start', '', url]
				subprocess.Popen(commands)
			elif sublime.platform() == 'linux':
				commands = ['xdg-open', url]
				subprocess.Popen(commands)
			else:
				commands = ['open', url]
				subprocess.Popen(commands)
			return
		except:
			pass

		sublime.error_message('Browser "'+browser+'" not found!\nIs installed? Which location...?')
