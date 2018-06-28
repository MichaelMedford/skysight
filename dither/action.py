#! /usr/bin/env python
#

""" Actions to be applied to a list of Camera CCDs. """

class Action():

	def __init__(self, degrees=0, xoff=0, yoff=0):
		self.degrees = degrees
		self.xoff = xoff
		self.yoff = yoff

	def apply(self, CCD):
		CCD.rotate(degrees=self.degrees)
		CCD.translate(xoff=self.xoff, yoff=self.yoff)

def action_CCDlist(CCDlist, action, name_arr):

	if type(name_arr[0]) in [int,np.int64]:
		name_arr = [str(n) for n in name_arr]

	for c in CCDlist:
		if c.name in name_arr:
			action.apply(c)

def remove_CCDlist(CCDlist, name_arr):

	if type(name_arr[0]) in [int,np.int64]:
		name_arr = [str(n) for n in name_arr]

	for c in CCDlist:
		if c.name in name_arr:
			CCDlist.remove(c)

def copy_CCDlist(CCDlist, name_arr):

	if type(name_arr[0]) in [int,np.int64]:
		name_arr = [str(n) for n in name_arr]

	new_list = []
	for name in name_arr:
		hsc_ccd = [c for c in CCDlist if c.name==name][0].copy()
		hsc_ccd.name = str(int(CCDlist[-1].name)+1)
		new_list.append(hsc_ccd.name)
		CCDlist.append(hsc_ccd)
	return CCDlist, new_list
