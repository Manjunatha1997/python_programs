
import torch
import os
import glob
import cv2
import numpy as np



class Colors:
    # Ultralytics color palette https://ultralytics.com/
    def __init__(self):
        # hex = matplotlib.colors.TABLEAU_COLORS.values()
        hex = ('FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', '1A9334', '00D4BB',
               '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', '520085', 'CB38FF', 'FF95C8', 'FF37C7')
        self.palette = [self.hex2rgb('#' + c) for c in hex]
        self.n = len(self.palette)

    def __call__(self, i, bgr=False):
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):  # rgb order (PIL)
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))


colors = Colors()  # create instance for 'from utils.plots import colors'





class Annotator:
	# if RANK in (-1, 0):
	#     check_font()  # download TTF if necessary

	# YOLOv5 Annotator for train/val mosaics and jpgs and detect/hub inference annotations
	def __init__(self, im, line_width=None, font_size=None, font='Arial.ttf', pil=False, example='abc'):
		assert im.data.contiguous, 'Image not contiguous. Apply np.ascontiguousarray(im) to Annotator() input images.'
		# self.pil = pil or not is_ascii(example) or is_chinese(example)
		# if self.pil:  # use PIL
		#     self.im = im if isinstance(im, Image.Image) else Image.fromarray(im)
		#     self.draw = ImageDraw.Draw(self.im)
		#     self.font = check_font(font='Arial.Unicode.ttf' if is_chinese(example) else font,
		#                            size=font_size or max(round(sum(self.im.size) / 2 * 0.035), 12))
		# else:  # use cv2
		self.im = im
		self.lw = line_width or max(round(sum(im.shape) / 2 * 0.003), 2)  # line width

	def box_label(self, box, label='', color=(128, 128, 128), txt_color=(255, 255, 255)):
		# Add one xyxy box to image with label
		if self.pil:# or not is_ascii(label):
			self.draw.rectangle(box, width=self.lw, outline=color)  # box
			if label:
				w, h = self.font.getsize(label)  # text width, height
				outside = box[1] - h >= 0  # label fits outside box
				self.draw.rectangle([box[0],
									 box[1] - h if outside else box[1],
									 box[0] + w + 1,
									 box[1] + 1 if outside else box[1] + h + 1], fill=color)
				# self.draw.text((box[0], box[1]), label, fill=txt_color, font=self.font, anchor='ls')  # for PIL>8.0
				self.draw.text((box[0], box[1] - h if outside else box[1]), label, fill=txt_color, font=self.font)
		else:  # cv2
			p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
			cv2.rectangle(self.im, p1, p2, color, thickness=self.lw, lineType=cv2.LINE_AA)
			if label:
				# if label == 'damage':
				#     label = 'd'
				tf = max(self.lw - 1, 1)  # font thickness
				w, h = cv2.getTextSize(label, 0, fontScale=self.lw / 3, thickness=tf)[0]  # text width, height
				outside = p1[1] - h - 3 >= 0  # label fits outside box
				p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
				cv2.rectangle(self.im, p1, p2, color, -1, cv2.LINE_AA)  # filled
				# cv2.putText(self.im, label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2), 0, self.lw / 3, txt_color,
				#             thickness=tf, lineType=cv2.LINE_AA)
				cv2.putText(self.im, label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2), 0, self.lw / 3, txt_color,
							thickness=tf, lineType=cv2.LINE_AA)
	def rectangle(self, xy, fill=None, outline=None, width=1):
		# Add rectangle to image (PIL-only)
		self.draw.rectangle(xy, fill, outline, width)

	def text(self, xy, text, txt_color=(255, 255, 255)):
		# Add text to image (PIL-only)
		w, h = self.font.getsize(text)  # text width, height
		self.draw.text((xy[0], xy[1] - h + 1), text, fill=txt_color, font=self.font)

	def result(self):
		# Return annotated image as array
		return np.asarray(self.im)



def run_inference_hub(hub_weights_path,image,conf=0.7):
	model = torch.hub.load('D:\\yolov5_auto','custom',path=hub_weights_path,source = 'local')
	model.conf = conf
	model.iou = 0.45

	# print(dir(model))

	results = model(image)

	labels = results.pandas().xyxy[0]
	labels = list(labels['name'])

	
	result_dict = results.pandas().xyxy[0].to_dict()

	annotator = Annotator(image, line_width=2, example=str(labels))

	tempo = []


	for k,v in result_dict.items():
		print(k,v)
		xmin = list(v.values())
		ymin = list(v.values())
		xmax = list(v.values())
		ymax = list(v.values())

		clss = list(v.values())
		name = list(v.values())

		tempo.append({'xyxy':[xmin,ymin,xmax,ymax]})
		tempo.append({'name':name})
		tempo.append({'c':clss})




	for i in tempo:
		print(i)
		print('*********************************')
		input()
		# annotator.box_label(xyxy, label, color=colors(c, True))

	# results.imgs
	# results.render()
	for img in results.imgs:
		return img, labels

predicted_image, detcetor_labels = run_inference_hub('yolov5s.pt',cv2.imread(r'D:\yolov5_auto\data\images\bus - Copy - Copy.jpg'))

# print(detcetor_labels)
# cv2.imshow('predected_image',predicted_image)
# cv2.waitKey(0)
