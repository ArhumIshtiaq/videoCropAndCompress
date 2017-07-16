import os
from moviepy.editor import *
from pyautogui import prompt, confirm
from moviepy.video.fx.crop import crop
from os.path import getsize, join, basename


def main(mp4=True, webm=True):

	global eligibleVidsEncountered, vidsCompressed, totalSizeOrig, totalSizeMP4,\
		totalSizeWebM, doWebM, doMP4

	doMP4 = mp4
	doWebM = webm

	eligibleVidsEncountered = 0
	vidsCompressed = 0

	totalSizeOrig = 0
	totalSizeMP4 = 0
	totalSizeWebM = 0

	if (doMP4 or doWebM):

		mainDir = prompt(text="Please enter the address of the directory that you want to compress the videos from:",
						 title="Video Directory", default="path/to/files")
		saveDir = prompt(text="Please enter the address of the directory that you want to compress the videos to:",
						 title="Compressed Video Directory", default="path/to/saved/files")
		suffix = prompt(text="Please enter the suffix of the video filename:",
						title="Filename Suffix", default="_CROPPED")

		for folder, subfolders, files in os.walk(mainDir):

			for file in files:

				fileDir = folder + "\\" + file

				fileSize = getsize(join(folder, file))

				if (file.endswith(suffix + ".mp4") or file.endswith(suffix + ".webm")):
					continue

				eligibleVidsEncountered += 1

				try:
					file = VideoFileClip(join(folder, file))

				except OSError:
					print("Sorry,", file, "wasn't converted.")
					pass

				totalSizeOrig += fileSize

				newFileDir = saveDir + basename(fileDir)[:-4] + suffix

				print("Cropping file:", basename(fileDir),
					  "to", basename(newFileDir))

				totalSizeMP4, totalSizeWebM = cropAndSaveFiles(
					file, newFileDir, totalSizeMP4, totalSizeWebM)

				vidsCompressed += 1

	else:
		print("No files were converted. Writing log and exitting program...")


def getFormat():
	choice = confirm(text="Choose file format:", title="File Format", buttons=[
					 "MP4", "WebM", "Both", "None"])

	if (choice == "MP4"):
		mp4, webm = True, False
	elif (choice == "WebM"):
		mp4, webm = False, True
	elif (choice == "Both"):
		mp4, webm = True, True
	elif (choice == "None"):
		mp4, webm = False, False

	return mp4, webm


def cropAndSaveFiles(file, newFileDir, totalSizeMP4, totalSizeWebM):
	cropFile = crop(file, x1=120, x2=720, y2=660)

	if (doMP4 == True):
		cropFile.write_videofile(
			newFileDir + ".mp4", fps=18, codec='libx264')
		totalSizeMP4 += getsize(newFileDir + ".mp4")

	if (doWebM == True):
		cropFile.write_videofile(
			newFileDir + ".webm", codec='libvpx')
		totalSizeWebM += getsize(newFileDir + ".webm")

	return totalSizeMP4, totalSizeWebM


if __name__ == '__main__':
	try:

		mp4, webm = getFormat()

		main(mp4=mp4, webm=webm)

		if (vidsCompressed > 0):

			totalSizeOrig = round(totalSizeOrig / 1000000, 2)
			totalSizeMP4 = round(totalSizeMP4 / 1000000, 2)
			totalSizeWebM = round(totalSizeWebM / 1000000, 2)

			averageSizeOrig = round(totalSizeOrig / eligibleVidsEncountered, 2)
			averageCompressionMP4 = round(totalSizeMP4 / vidsCompressed, 2)
			averageCompressionWebM = round(totalSizeWebM / vidsCompressed, 2)

		with open("vidCompressionData.txt", 'a') as logFile:
			if (vidsCompressed > 0):
				logFile.write("No. of (Eligible) Videos Encountered: " +
							  str(eligibleVidsEncountered) + "\n")
				logFile.write("No. of Videos Compressed: " +
							  str(vidsCompressed) + "\n")
				logFile.write(
					"Total Uncropped Original Video Size: " + str(totalSizeOrig) + "MB\n")

				if (doMP4 == True):
					logFile.write("\n")
					logFile.write(
						"Total Cropped Video Size (MP4): " + str(totalSizeMP4) + "MB\n")
					logFile.write("Average MP4 Compression: From " + str(
						averageSizeOrig) + "MB to " + str(averageCompressionMP4) + "MB\n")
					logFile.write("Total MP4 Compression: From " +
								  str(totalSizeOrig) + "MB to " + str(totalSizeMP4) + "MB" + "\n")
					logFile.write("Compression Factor: " +
								  str(round(totalSizeOrig / totalSizeMP4, 2)) + "times!\n")

				if (doWebM == True):
					logFile.write("\n")
					logFile.write("Total Cropped Video Size (WebM): " +
								  str(totalSizeWebM) + "MB" + "\n")
					logFile.write("Average WebM Compression: From " + str(
						averageSizeOrig) + "MB to " + str(averageCompressionWebM) + "MB\n")
					logFile.write("Total WebM Compression: From " +
								  str(totalSizeOrig) + "MB to " + str(totalSizeWebM) + "MB\n")
					logFile.write(
						"Compression Factor: " + str(round(totalSizeOrig / totalSizeWebM, 2)) + "times!\n")

				logFile.write("*" * 50 + "\n")

			else:
				logFile.write("No files were converted into .mp4 or .webm \n")
				logFile.write("*" * 50 + "\n")

	except Exception as e:
		raise e
		print("An error occured:", e)
		pass
