import sublime, sublime_plugin
from subprocess import PIPE, Popen

class TexcountCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		filename = self.view.file_name()

		if filename == None:
			sublime.error_message("No file selected")
			return

		filename = filename.replace(" ","\ ")
		cmd = "texcount " + filename

		# MacTex fix
		cmd = "PATH=$PATH:/usr/texbin; " + cmd

		testcmdprocess = Popen("PATH=$PATH:/usr/texbin; which texcount", shell=True, stdout=PIPE, stderr=PIPE)
		testout, testerr = testcmdprocess.communicate()
		if (testout == ""):
			sublime.error_message("TeXcount not installed in PATH \nDownload from: http://app.uio.no/ifi/texcount/")
			return

		p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
		out, err = p.communicate()

		if (self.view.is_dirty()):
			out = out + "\nWarning, File not up to date!"

		sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})
		out = out.strip()
		print(out)
		return
