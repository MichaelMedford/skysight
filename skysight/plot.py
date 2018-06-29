#! /usr/bin/env python
#

""" Plots of dithers applied to cameras. """

import matplotlib.pyplot as plt

def two_exposures_plot(camera, slewList):

	cameraA = camera.copy()
	cameraB = camera.copy()

	slewList[0].apply(cameraA)
	slewList[1].apply(cameraB)

	cameraAB = cameraA.intersect(cameraB)

	area1 = cameraA.difference(cameraAB).get_area()
	area1 += cameraB.difference(cameraAB).get_area()

	area2 = cameraAB.get_area()

	cameraABunion = cameraA.union(cameraB)
	xlim, ylim = cameraABunion.get_limits()

	fig, ax = plt.subplots(2, 2, figsize=(8,8))
	fig.suptitle('Two Exposures Plot', fontsize = 20)
	ax = ax.flatten()

	cameraA.plot(ax[0],
				 color = 'r',
				 alpha = 0.3,
				 xlim = xlim,
				 ylim = ylim)
	cameraB.plot(ax[0],
				 color = 'g',
				 alpha = 0.3,
				 xlim = xlim,
				 ylim = ylim)
	ax[0].set_title('All Exposures  %.2f deg$^2$' % cameraABunion.get_area())
	ax[0].axis('off')

	cameraAOnly = cameraA.difference(cameraAB)
	cameraAOnly.plot(ax[1],
					 color = 'r',
					 alpha = 0.3,
					 xlim = xlim,
					 ylim = ylim)
	ax[1].set_title('1st Slew Only  %.2f deg$^2$' % cameraAOnly.get_area())
	ax[1].axis('off')

	cameraBOnly = cameraB.difference(cameraAB)
	cameraBOnly.plot(ax[2],
					 color = 'g',
					 alpha = 0.3,
					 xlim = xlim,
					 ylim = ylim)
	ax[2].set_title('2nd Slew Only  %.2f deg$^2$' % cameraBOnly.get_area())
	ax[2].axis('off')

	cameraAB.plot(ax[3],
				  color = 'c',
				  alpha = 0.3,
				  xlim = xlim,
				  ylim = ylim)
	ax[3].set_title('Both Slew  %.2f deg$^2$' % cameraAB.get_area())
	ax[3].axis('off')

	fig.text(0.75, .05,
			 'Two Exposures  %.2f deg$^2$' % area2,
			 fontsize = 15,
			 horizontalalignment = 'center')
	fig.text(0.25, .05,
			 'One Exposure  %.2f deg$^2$' % area1,
			 fontsize = 15,
			 horizontalalignment = 'center')


def three_exposures_plot(camera, slewList):

	cameraA = camera.copy()
	cameraB = camera.copy()
	cameraC = camera.copy()

	slewList[0].apply(cameraA)
	slewList[1].apply(cameraB)
	slewList[2].apply(cameraC)

	cameraAB = cameraA.intersect(cameraB)
	cameraBC = cameraB.intersect(cameraC)
	cameraAC = cameraA.intersect(cameraC)

	cameraABC = cameraAC.intersect(cameraB)

	cameraAOnly = cameraA.difference(cameraB.union(cameraC))
	cameraBOnly = cameraB.difference(cameraA.union(cameraC))
	cameraCOnly = cameraC.difference(cameraA.union(cameraB))

	area1 = cameraAOnly.get_area()
	area1 += cameraBOnly.get_area()
	area1 += cameraCOnly.get_area()

	cameraABOnly = cameraAB.difference(cameraABC)
	cameraACOnly = cameraAC.difference(cameraABC)
	cameraBCOnly = cameraBC.difference(cameraABC)

	area2 = cameraABOnly.get_area()
	area2 += cameraACOnly.get_area()
	area2 += cameraBCOnly.get_area()

	area3 = cameraABC.get_area()

	cameraAll = cameraA.union(cameraB).union(cameraC)
	xlim, ylim = cameraAll.get_limits()

	fig, ax = plt.subplots(3, 3, figsize=(8,8))
	fig.suptitle('Three Exposures Plot', fontsize = 20)
	ax = ax.flatten()

	cameraA.plot(ax[0],
				 color = 'r',
				 alpha = 0.3,
				 xlim = xlim,
				 ylim = ylim)
	cameraB.plot(ax[0],
				 color = 'g',
				 alpha = 0.3,
				 xlim = xlim,
				 ylim = ylim)
	cameraC.plot(ax[0],
				 color = 'b',
				 alpha = 0.3,
				 xlim = xlim,
				 ylim = ylim)
	ax[0].set_title('All Exposures  %.2f deg$^2$' % cameraAll.get_area(),
					fontsize = 10)
	ax[0].axis('off')

	cameraAOnly.plot(ax[1],
					 color = 'r',
					 alpha = 0.3,
					 xlim = xlim,
					 ylim = ylim)
	ax[1].set_title('1st Slew Only  %.2f deg$^2$' % cameraAOnly.get_area(),
					fontsize = 10)
	ax[1].axis('off')

	cameraBOnly.plot(ax[2],
					 color = 'g',
					 alpha = 0.3,
					 xlim = xlim,
					 ylim = ylim)
	ax[2].set_title('2nd Slew Only  %.2f deg$^2$' % cameraBOnly.get_area(),
					fontsize = 10)
	ax[2].axis('off')

	cameraCOnly.plot(ax[3],
					 color = 'b',
					 alpha = 0.3,
					 xlim = xlim,
					 ylim = ylim)
	ax[3].set_title('3rd Slew Only  %.2f deg$^2$' % cameraCOnly.get_area(),
					fontsize = 10)
	ax[3].axis('off')

	cameraABOnly.plot(ax[4],
					  color = 'c',
					  alpha = 0.3,
					  xlim = xlim,
					  ylim = ylim)
	ax[4].set_title('1st/2nd Slews Only  %.2f deg$^2$' % cameraABOnly.get_area(),
					fontsize = 10)
	ax[4].axis('off')

	cameraACOnly.plot(ax[5],
					  color = 'm',
					  alpha = 0.3,
					  xlim = xlim,
					  ylim = ylim)
	ax[5].set_title('1st/3rd Slews Only  %.2f deg$^2$' % cameraACOnly.get_area(),
					fontsize = 10)
	ax[5].axis('off')

	cameraBCOnly.plot(ax[6],
					  color = 'y',
					  alpha = 0.3,
					  xlim = xlim,
					  ylim = ylim)
	ax[6].set_title('2nd/3rd Slews Only  %.2f deg$^2$' % cameraBCOnly.get_area(),
					fontsize = 10)
	ax[6].axis('off')

	cameraABC.plot(ax[7],
				   color = 'k',
				   alpha = 0.3,
				   xlim = xlim,
				   ylim = ylim)
	ax[7].set_title('All Slews  %.2f deg$^2$' % cameraABC.get_area(),
					fontsize = 10)
	ax[7].axis('off')

	ax[8].axis('off')

	fig.text(.75, 0.05,
			 'Three Exposures  %.2f deg$^2$' % area3,
			 fontsize = 10,
			 horizontalalignment = 'center')
	fig.text(.5, 0.05,
			 'Two Exposures  %.2f deg$^2$' % area2,
			 fontsize = 10,
			 horizontalalignment = 'center')
	fig.text(.25, 0.05,
			 'One Exposure  %.2f deg$^2$' % area1,
			 fontsize = 10,
			 horizontalalignment = 'center')
