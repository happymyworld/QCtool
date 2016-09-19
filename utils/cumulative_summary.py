#!/usr/bin/env python

import sys
import os
import getopt
import commands
import re
import glob

def atoi(text):
	return int(text) if text.isdigit() else text

def natural_keys(text):
	'''
	alist.sort(key=natural_keys) sorts in human order
	http://nedbatchelder.com/blog/200712/human_sorting.html
	(See Toothy's implementation in the comments)
	'''
	return [ atoi(c) for c in re.split('(\d+)', text) ]


def minigraph(path, reads):

	rscript=open('%s/rtemp.R'%path,'a')
	rscript.write("""

filename <- "%s/temp_linecount.txt"				  
countlines<-read.table(filename, header=FALSE)

subplot(rect(par("usr")[1], par("usr")[3], par("usr")[2], par("usr")[4], col = "white"),x=length(d1$read_length)/10, y=0.32, size=c(1.5,2.2), inset=0)
subplot(boxplot(countlines$V2, data=countlines,  xaxt='n', yaxt='n', ylim=c(0, max(countlines$V2)), col = "white", bg = "white", outline=FALSE),x=length(d1$read_length)/10, y=0.32, size=c(1.5,2.2), inset=0)
subplot(stripchart(countlines$V2, frame.plot=FALSE, tck=0.02, mgp=c(-1,-1.7,0), cex.axis=0.5, las=1, xaxt='n', vertical = TRUE, method = "jitter", pch = 21, cex=0.7, col='black', bg = cl), x=length(d1$read_length)/10, y=0.32, vadj=0.5, size=c(1.5,2))

				  """%(path))
	rscript.close()

def basegraph(file1,readname, groupname, n, undetfound):
	rscript=open('%s/rtemp.R'%path,'w')
	rscript.write("""
library(RColorBrewer)
library(package=grid)
	lo = function(rown, coln, nrow, ncol, cellheight = NA, cellwidth = NA, treeheight_col, treeheight_row, legend, annotation, annotation_colors, annotation_legend, main, fontsize, fontsize_row, fontsize_col, ...){
	  # Get height of colnames and length of rownames
	  if(!is.null(coln[1])){
	    longest_coln = which.max(nchar(coln))
	    gp = list(fontsize = fontsize_col, ...)
	    coln_height = unit(1.1, "grobheight", textGrob(coln[longest_coln], rot = 90, gp = do.call(gpar, gp)))
	  }
	  else{
	    coln_height = unit(5, "bigpts")
	  }

	  if(!is.null(rown[1])){
	    longest_rown = which.max(nchar(rown))
	    gp = list(fontsize = fontsize_row, ...)
	    rown_width = unit(1.2, "grobwidth", textGrob(rown[longest_rown], gp = do.call(gpar, gp)))
	  }
	  else{
	    rown_width = unit(5, "bigpts")
	  }

	  gp = list(fontsize = fontsize, ...)
	  # Legend position
	  if(!is.na(legend[1])){
	    longest_break = which.max(nchar(names(legend)))
	    longest_break = unit(1.1, "grobwidth", textGrob(as.character(names(legend))[longest_break], gp = do.call(gpar, gp)))
	    title_length = unit(1.1, "grobwidth", textGrob("Scale", gp = gpar(fontface = "bold", ...)))
	    legend_width = unit(12, "bigpts") + longest_break * 1.2
	    legend_width = max(title_length, legend_width)
	  }
	  else{
	    legend_width = unit(0, "bigpts")
	  }

	  # Set main title height
	  if(is.na(main)){
	    main_height = unit(0, "npc")
	  }
	  else{
	    main_height = unit(5.5, "grobheight", textGrob(main, gp = gpar(fontsize = 1.3 * fontsize, ...)))
	  }

	  # Column annotations
	  if(!is.na(annotation[[1]][1])){
	    # Column annotation height 
	    annot_height = unit(ncol(annotation) * (8 + 2) + 2, "bigpts")
	    # Width of the correponding legend
	    longest_ann = which.max(nchar(as.matrix(annotation)))
	    annot_legend_width = unit(1.2, "grobwidth", textGrob(as.matrix(annotation)[longest_ann], gp = gpar(...))) + unit(12, "bigpts")
	    if(!annotation_legend){
	      annot_legend_width = unit(0, "npc")
	    }
	  }
	  else{
	    annot_height = unit(0, "bigpts")
	    annot_legend_width = unit(0, "bigpts")
	  }

	  # Tree height
	  treeheight_col = unit(treeheight_col, "bigpts") + unit(5, "bigpts")
	  treeheight_row = unit(treeheight_row, "bigpts") + unit(5, "bigpts") 

	  # Set cell sizes
	  if(is.na(cellwidth)){
	    matwidth = unit(1, "npc") - rown_width - legend_width - treeheight_row - annot_legend_width
	  }
	  else{
	    matwidth = unit(cellwidth * ncol, "bigpts")
	  }

	  if(is.na(cellheight)){
	    matheight = unit(1, "npc") - main_height - coln_height - treeheight_col - annot_height
	  }
	  else{
	    matheight = unit(cellheight * nrow, "bigpts")
	  }	


	  # Produce layout()
	  pushViewport(viewport(layout = grid.layout(nrow = 5, ncol = 6, widths = unit.c(treeheight_row, matwidth, rown_width, legend_width, annot_legend_width), heights = unit.c(main_height, treeheight_col, annot_height, matheight, coln_height)), gp = do.call(gpar, gp)))

	  # Get cell dimensions
	  pushViewport(vplayout(4, 2))
	  cellwidth = convertWidth(unit(0:1, "npc"), "bigpts", valueOnly = T)[2] / ncol
	  cellheight = convertHeight(unit(0:1, "npc"), "bigpts", valueOnly = T)[2] / nrow
	  upViewport()

	  # Return minimal cell dimension in bigpts to decide if borders are drawn
	  mindim = min(cellwidth, cellheight) 
	  return(mindim)
	}

	draw_dendrogram = function(hc, horizontal = T){
	  h = hc$height / max(hc$height) / 1.05
	  m = hc$merge
	  o = hc$order
	  n = length(o)

	  m[m > 0] = n + m[m > 0] 
	  m[m < 0] = abs(m[m < 0])

	  dist = matrix(0, nrow = 2 * n - 1, ncol = 2, dimnames = list(NULL, c("x", "y"))) 
	  dist[1:n, 1] = 1 / n / 2 + (1 / n) * (match(1:n, o) - 1)

	  for(i in 1:nrow(m)){
	    dist[n + i, 1] = (dist[m[i, 1], 1] + dist[m[i, 2], 1]) / 2
	    dist[n + i, 2] = h[i]
	  }

	  draw_connection = function(x1, x2, y1, y2, y){
	    grid.lines(x = c(x1, x1), y = c(y1, y))
	    grid.lines(x = c(x2, x2), y = c(y2, y))
	    grid.lines(x = c(x1, x2), y = c(y, y))
	  }

	  if(horizontal){
	    for(i in 1:nrow(m)){
	      draw_connection(dist[m[i, 1], 1], dist[m[i, 2], 1], dist[m[i, 1], 2], dist[m[i, 2], 2], h[i])
	    }
	  }

	  else{
	    gr = rectGrob()
	    pushViewport(viewport(height = unit(1, "grobwidth", gr), width = unit(1, "grobheight", gr), angle = 90))
	    dist[, 1] = 1 - dist[, 1] 
	    for(i in 1:nrow(m)){
	      draw_connection(dist[m[i, 1], 1], dist[m[i, 2], 1], dist[m[i, 1], 2], dist[m[i, 2], 2], h[i])
	    }
	    upViewport()
	  }
	}

	draw_matrix = function(matrix, border_color, fmat, fontsize_number){
	  n = nrow(matrix)
	  m = ncol(matrix)
	  x = (1:m)/m - 1/2/m
	  y = 1 - ((1:n)/n - 1/2/n)
	  for(i in 1:m){
	    grid.rect(x = x[i], y = y[1:n], width = 1/m, height = 1/n, gp = gpar(fill = matrix[,i], col = border_color))
	    if(attr(fmat, "draw")){
	      grid.text(x = x[i], y = y[1:n], label = fmat[, i], gp = gpar(col = "grey30", fontsize = fontsize_number))
	    }
	  }
	}

	draw_colnames = function(coln, ...){
	  m = length(coln)
	  x = (1:m)/m - 1/2/m
	  grid.text(coln, x = x, y = unit(0.96, "npc"), vjust = 0.5, hjust = 0, rot = 270, gp = gpar(...))
	}

	draw_rownames = function(rown, ...){
	  n = length(rown)
	  y = 1 - ((1:n)/n - 1/2/n)
	  grid.text(rown, x = unit(0.04, "npc"), y = y, vjust = 0.5, hjust = 0, gp = gpar(...))	
	}

	draw_titles = function(rown, ...){
	n = length(rown)
	y = 3 - ((1:n)/n - 1/2/n)
	grid.text(rown, x = unit(0.04, \"npc\"), y = y, vjust = 0.5, hjust = 0, gp = gpar(fontface='bold', ...))
	}

	draw_legend = function(color, breaks, legend, ...){
	  height = min(unit(1, "npc"), unit(150, "bigpts"))
	  pushViewport(viewport(x = 0, y = unit(1, "npc"), just = c(0, 1), height = height))
	  legend_pos = (legend - min(breaks)) / (max(breaks) - min(breaks))
	  breaks = (breaks - min(breaks)) / (max(breaks) - min(breaks))
	  h = breaks[-1] - breaks[-length(breaks)]
	  grid.rect(x = 0, y = breaks[-length(breaks)], width = unit(10, "bigpts"), height = h, hjust = 0, vjust = 0, gp = gpar(fill = color, col = "#FFFFFF00"))
	  grid.text(names(legend), x = unit(12, "bigpts"), y = legend_pos, hjust = 0, gp = gpar(...))
	  upViewport()
	}

	convert_annotations = function(annotation, annotation_colors){
	  new = annotation
	  for(i in 1:ncol(annotation)){
	    a = annotation[, i]
	    b = annotation_colors[[colnames(annotation)[i]]]
	    if(is.character(a) | is.factor(a)){
	      a = as.character(a)
	      if(length(setdiff(a, names(b))) > 0){
		stop(sprintf("Factor levels on variable %%s do not match with annotation_colors", colnames(annotation)[i]))
	      }
	      new[, i] = b[a]
	    }
	    else{
	      a = cut(a, breaks = 100)
	      new[, i] = colorRampPalette(b)(100)[a]
	    }
	  }
	  return(as.matrix(new))
	}

	draw_annotations = function(converted_annotations, border_color){
	  n = ncol(converted_annotations)
	  m = nrow(converted_annotations)
	  x = (1:m)/m - 1/2/m
	  y = cumsum(rep(8, n)) - 4 + cumsum(rep(2, n))
	  for(i in 1:m){
	    grid.rect(x = x[i], unit(y[1:n], "bigpts"), width = 1/m, height = unit(8, "bigpts"), gp = gpar(fill = converted_annotations[i, ], col = border_color))
	  }
	}

	draw_annotation_legend = function(annotation, annotation_colors, border_color, ...){
	  y = unit(1, "npc")
	  text_height = unit(1, "grobheight", textGrob("FGH", gp = gpar(...)))
	  for(i in names(annotation_colors)){
	    grid.text(i, x = 0, y = y, vjust = 1, hjust = 0, gp = gpar(fontface = "bold", ...))
	    y = y - 1.5 * text_height
	    if(is.character(annotation[, i]) | is.factor(annotation[, i])){
	      for(j in 1:length(annotation_colors[[i]])){
		grid.rect(x = unit(0, "npc"), y = y, hjust = 0, vjust = 1, height = text_height, width = text_height, gp = gpar(col = border_color, fill = annotation_colors[[i]][j]))
		grid.text(names(annotation_colors[[i]])[j], x = text_height * 1.3, y = y, hjust = 0, vjust = 1, gp = gpar(...))
		y = y - 1.5 * text_height
	      }
	    }
	    else{
	      yy = y - 4 * text_height + seq(0, 1, 0.02) * 4 * text_height
	      h = 4 * text_height * 0.02
	      grid.rect(x = unit(0, "npc"), y = yy, hjust = 0, vjust = 1, height = h, width = text_height, gp = gpar(col = "#FFFFFF00", fill = colorRampPalette(annotation_colors[[i]])(50)))
	      txt = rev(range(grid.pretty(range(annotation[, i], na.rm = TRUE))))
	      yy = y - c(0, 3) * text_height
	      grid.text(txt, x = text_height * 1.3, y = yy, hjust = 0, vjust = 1, gp = gpar(...))
	      y = y - 4.5 * text_height
	    }
	    y = y - 1.5 * text_height
	  }
	}
	draw_main = function(text, ...){
	  grid.text(text, gp = gpar(fontface = "bold", ...))
	}

	vplayout = function(x, y){
	  return(viewport(layout.pos.row = x, layout.pos.col = y))
	}

	heatmap_motor = function(matrix, border_color, cellwidth, cellheight, tree_col, tree_row, treeheight_col, treeheight_row, filename, width, height, breaks, color, legend, annotation, annotation_colors, annotation_legend, main, fontsize, fontsize_row, fontsize_col, fmat, fontsize_number, ...){
	  grid.newpage()

	  # Set layout
	  mindim = lo(coln = colnames(matrix), rown = rownames(matrix), nrow = nrow(matrix), ncol = ncol(matrix), cellwidth = cellwidth, cellheight = cellheight, treeheight_col = treeheight_col, treeheight_row = treeheight_row, legend = legend, annotation = annotation, annotation_colors = annotation_colors, annotation_legend = annotation_legend, main = main, fontsize = fontsize, fontsize_row = fontsize_row, fontsize_col = fontsize_col,  ...)

	  if(!is.na(filename)){
	    pushViewport(vplayout(1:5, 1:5))

	    if(is.na(height)){
	      height = convertHeight(unit(0:1, "npc"), "inches", valueOnly = T)[2]
	    }
	    if(is.na(width)){
	      width = convertWidth(unit(0:1, "npc"), "inches", valueOnly = T)[2]
	    }

	    # Get file type
	    r = regexpr("\\\\.[a-zA-Z]*$", filename)
	    if(r == -1) stop("Improper filename")
	    ending = substr(filename, r + 1, r + attr(r, "match.length"))

	    f = switch(ending,
		       pdf = function(x, ...) pdf(x, ...),
		       png = function(x, ...) png(x, units = "in", res = 300, ...),
		       jpeg = function(x, ...) jpeg(x, units = "in", res = 300, ...),
		       jpg = function(x, ...) jpeg(x, units = "in", res = 300, ...),
		       tiff = function(x, ...) tiff(x, units = "in", res = 300, compression = "lzw", ...),
		       bmp = function(x, ...) bmp(x, units = "in", res = 300, ...),
		       stop("File type should be: pdf, png, bmp, jpg, tiff")
	    )

	    # print(sprintf("height:%%f width:%%f", height, width))
	    f(filename, height = height+1.5, width = width+1)
	    heatmap_motor(matrix, cellwidth = cellwidth, cellheight = cellheight, border_color = border_color, tree_col = tree_col, tree_row = tree_row, treeheight_col = treeheight_col, treeheight_row = treeheight_row, breaks = breaks, color = color, legend = legend, annotation = annotation, annotation_colors = annotation_colors, annotation_legend = annotation_legend, filename = NA, main = main, fontsize = fontsize, fontsize_row = fontsize_row, fontsize_col = fontsize_col, fmat = fmat, fontsize_number =  fontsize_number, ...)
	    garbage<-dev.off()
	    upViewport()
	    return()
	  }

	  # Omit border color if cell size is too small 
	  if(mindim < 3) border_color = NA

	  # Draw title
	  if(!is.na(main)){
	    pushViewport(vplayout(1, 2))
	    draw_main(main, fontsize = 1.6 * fontsize, ...)
	    upViewport()
	  }

	  # Draw tree for the columns
	  if(!is.na(tree_col[[1]][1]) & treeheight_col != 0){
	    pushViewport(vplayout(2, 2))
	    draw_dendrogram(tree_col, horizontal = T)
	    upViewport()
	  }

	  # Draw tree for the rows
	  if(!is.na(tree_row[[1]][1]) & treeheight_row != 0){
	    pushViewport(vplayout(4, 1))
	    draw_dendrogram(tree_row, horizontal = F)
	    upViewport()
	  }

	  # Draw matrix
	  pushViewport(vplayout(4, 2))
	  draw_matrix(matrix, border_color, fmat, fontsize_number)
	  upViewport()

	  # Draw colnames
	  if(length(colnames(matrix)) != 0){
	    pushViewport(vplayout(5, 2))
	    pars = list(colnames(matrix), fontsize = fontsize_col, ...)
	    do.call(draw_colnames, pars)
	    upViewport()
	  }

	  # Draw rownames
	  if(length(rownames(matrix)) != 0){
	    pushViewport(vplayout(4, 3))
	    pars = list(rownames(matrix), fontsize = fontsize_row, ...)
	    do.call(draw_rownames, pars)
	    upViewport()
	  }

	  # Draw titles
	  pushViewport(vplayout(2, 3))
	  pars = list(c("Avg     Sample"), fontsize = fontsize_row, ...)
	  do.call(draw_titles, pars)
	  upViewport()

	  # Draw annotation tracks
	  if(!is.na(annotation[[1]][1])){
	    pushViewport(vplayout(3, 2))
	    converted_annotation = convert_annotations(annotation, annotation_colors)
	    draw_annotations(converted_annotation, border_color)
	    upViewport()
	  }

	  # Draw annotation legend
	  if(!is.na(annotation[[1]][1]) & annotation_legend){
	    if(length(rownames(matrix)) != 0){
	      pushViewport(vplayout(4:5, 5))
	    }
	    else{
	      pushViewport(vplayout(3:5, 5))
	    }
	    draw_annotation_legend(annotation, annotation_colors, border_color, fontsize = fontsize, ...)
	    upViewport()
	  }

	  # Draw legend
	  if(!is.na(legend[1])){
	    length(colnames(matrix))
	    if(length(rownames(matrix)) != 0 && length(rownames(matrix))>3){
	      pushViewport(vplayout(4:5, 5))
	    }else if(length(rownames(matrix))!= 0 && length(rownames(matrix))<3){
	      pushViewport(vplayout(1:5, 5))
	    }else{
	      pushViewport(vplayout(3:5, 5))
	    }
	    draw_legend(color, breaks, legend, fontsize = fontsize, ...)
	    upViewport()
	  }


	}

	generate_breaks = function(x, n){
	  seq(min(x, na.rm = T), max(x, na.rm = T), length.out = n + 1)
	}

	scale_vec_colours = function(x, col = rainbow(10), breaks = NA){
	  return(col[as.numeric(cut(x, breaks = breaks, include.lowest = T))])
	}

	scale_colours = function(mat, col = rainbow(10), breaks = NA){
	  mat = as.matrix(mat)
	  return(matrix(scale_vec_colours(as.vector(mat), col = col, breaks = breaks), nrow(mat), ncol(mat), dimnames = list(rownames(mat), colnames(mat))))
	}

	cluster_mat = function(mat, distance, method){
	  if(!(method %%in%% c("ward", "single", "complete", "average", "mcquitty", "median", "centroid"))){
	    stop("clustering method has to one form the list: 'ward', 'single', 'complete', 'average', 'mcquitty', 'median' or 'centroid'.")
	  }
	  if(!(distance[1] %%in%% c("correlation", "euclidean", "maximum", "manhattan", "canberra", "binary", "minkowski")) & class(distance) != "dist"){
	    print(!(distance[1] %%in%% c("correlation", "euclidean", "maximum", "manhattan", "canberra", "binary", "minkowski")) | class(distance) != "dist")
	    stop("distance has to be a dissimilarity structure as produced by dist or one measure  form the list: 'correlation', 'euclidean', 'maximum', 'manhattan', 'canberra', 'binary', 'minkowski'")
	  }
	  if(distance[1] == "correlation"){
	    d = dist(1 - cor(t(mat)))
	  }
	  else{
	    if(class(distance) == "dist"){
	      d = distance
	    }
	    else{
	      d = dist(mat, method = distance)
	    }
	  }

	  return(hclust(d, method = method))
	}

	scale_rows = function(x){
	  m = apply(x, 1, mean, na.rm = T)
	  s = apply(x, 1, sd, na.rm = T)
	  return((x - m) / s)
	}

	scale_mat = function(mat, scale){
	  if(!(scale %%in%% c("none", "row", "column"))){
	    stop("scale argument shoud take values: 'none', 'row' or 'column'")
	  }
	  mat = switch(scale, none = mat, row = scale_rows(mat), column = t(scale_rows(t(mat))))
	  return(mat)
	}

	generate_annotation_colours = function(annotation, annotation_colors, drop){
	  if(is.na(annotation_colors)[[1]][1]){
	    annotation_colors = list()
	  }
	  count = 0
	  for(i in 1:ncol(annotation)){
	    if(is.character(annotation[, i]) | is.factor(annotation[, i])){
	      if (is.factor(annotation[, i]) & !drop){
		count = count + length(levels(annotation[, i]))
	      }
	      count = count + length(unique(annotation[, i]))
	    }
	  }

	  factor_colors = hsv((seq(0, 1, length.out = count + 1)[-1] + 
	    0.2)%%%%1, 0.7, 0.95)

	  set.seed(3453)

	  for(i in 1:ncol(annotation)){
	    if(!(colnames(annotation)[i] %%in%% names(annotation_colors))){
	      if(is.character(annotation[, i]) | is.factor(annotation[, i])){
		n = length(unique(annotation[, i]))
		if (is.factor(annotation[, i]) & !drop){
		  n = length(levels(annotation[, i]))
		}
		ind = sample(1:length(factor_colors), n)
		annotation_colors[[colnames(annotation)[i]]] = factor_colors[ind]
		l = levels(as.factor(annotation[, i]))
		l = l[l %%in%% unique(annotation[, i])]
		if (is.factor(annotation[, i]) & !drop){
		  l = levels(annotation[, i])
		}
		names(annotation_colors[[colnames(annotation)[i]]]) = l
		factor_colors = factor_colors[-ind]
	      }
	      else{
		r = runif(1)
		annotation_colors[[colnames(annotation)[i]]] = hsv(r, c(0.1, 1), 1)
	      }
	    }
	  }
	  return(annotation_colors)
	}

	kmeans_pheatmap = function(mat, k = min(nrow(mat), 150), sd_limit = NA, ...){
	  # Filter data
	  if(!is.na(sd_limit)){
	    s = apply(mat, 1, sd)
	    mat = mat[s > sd_limit, ]	
	  }

	  # Cluster data
	  set.seed(1245678)
	  km = kmeans(mat, k, iter.max = 100)
	  mat2 = km$centers

	  # Compose rownames
	  t = table(km$cluster)
	  rownames(mat2) = sprintf("cl%%s_size_%%d", names(t), t)

	  # Draw heatmap
	  pheatmap(mat2, ...)
	}

	pheatmap = function(mat, color = colorRampPalette(rev(c("#D73027", "#FC8D59", "#FEE090", "#FFFFBF", "#E0F3F8", "#91BFDB", "#4575B4")))(100), kmeans_k = NA, breaks = NA, border_color = "grey60", cellwidth = NA, cellheight = NA, scale = "none", cluster_rows = TRUE, cluster_cols = TRUE, clustering_distance_rows = "euclidean", clustering_distance_cols = "euclidean", clustering_method = "complete",  treeheight_row = ifelse(cluster_rows, 50, 0), treeheight_col = ifelse(cluster_cols, 50, 0), legend = TRUE, legend_breaks = NA, legend_labels = NA, annotation = NA, annotation_colors = NA, annotation_legend = TRUE, drop_levels = TRUE, show_rownames = T, show_colnames = T, main = NA, fontsize = 10, fontsize_row = fontsize, fontsize_col = fontsize, display_numbers = F, number_format = "%%.2f", fontsize_number = 0.8 * fontsize, filename = NA, width = NA, height = NA, ...){

	  # Preprocess matrix
	  mat = as.matrix(mat)
	  mat = scale_mat(mat, scale)

	  # Kmeans
	  if(!is.na(kmeans_k)){
	    # Cluster data
	    km = kmeans(mat, kmeans_k, iter.max = 100)
	    mat = km$centers

	    # Compose rownames
	    t = table(km$cluster)
	    rownames(mat) = sprintf("cl%%s_size_%%d", names(t), t)
	  }
	  else{
	    km = NA
	  }

	  # Do clustering
	  if(cluster_rows){
	    tree_row = cluster_mat(mat, distance = clustering_distance_rows, method = clustering_method)
	    mat = mat[tree_row$order, ]
	  }
	  else{
	    tree_row = NA
	    treeheight_row = 0
	  }

	  if(cluster_cols){
	    tree_col = cluster_mat(t(mat), distance = clustering_distance_cols, method = clustering_method)
	    mat = mat[, tree_col$order]
	  }
	  else{
	    tree_col = NA
	    treeheight_col = 0
	  }

	  # Format numbers to be displayed in cells 
	  if(display_numbers){
	    fmat = matrix(sprintf(number_format, mat), nrow = nrow(mat), ncol = ncol(mat))
	    attr(fmat, "draw") = TRUE
	  }
	  else{
	    fmat = matrix(NA, nrow = nrow(mat), ncol = ncol(mat))
	    attr(fmat, "draw") = FALSE
	  }


	  # Colors and scales
	  if(!is.na(legend_breaks[1]) & !is.na(legend_labels[1])){
	    if(length(legend_breaks) != length(legend_labels)){
	      stop("Lengths of legend_breaks and legend_labels must be the same")
	    }
	  }


	  if(is.na(breaks[1])){
	    breaks = generate_breaks(as.vector(mat), length(color))
	  }
	  if (legend & is.na(legend_breaks[1])) {
	    legend = grid.pretty(range(as.vector(breaks)))
	    names(legend) = legend
	  }
	  else if(legend & !is.na(legend_breaks[1])){
	    legend = legend_breaks[legend_breaks >= min(breaks) & legend_breaks <= max(breaks)]

	    if(!is.na(legend_labels[1])){
	      legend_labels = legend_labels[legend_breaks >= min(breaks) & legend_breaks <= max(breaks)]
	      names(legend) = legend_labels
	    }
	    else{
	      names(legend) = legend
	    }
	  }
	  else {
	    legend = NA
	  }
	  mat = scale_colours(mat, col = color, breaks = breaks)

	  # Preparing annotation colors
	  if(!is.na(annotation[[1]][1])){
	    annotation = annotation[colnames(mat), , drop = F]
	    annotation_colors = generate_annotation_colours(annotation, annotation_colors, drop = drop_levels)
	  }

	  if(!show_rownames){
	    rownames(mat) = NULL
	  }

	  if(!show_colnames){
	    colnames(mat) = NULL
	  }

	  # Draw heatmap
	  heatmap_motor(mat, border_color = border_color, cellwidth = cellwidth, cellheight = cellheight, treeheight_col = treeheight_col, treeheight_row = treeheight_row, tree_col = tree_col, tree_row = tree_row, filename = filename, width = width, height = height, breaks = breaks, color = color, legend = legend, annotation = annotation, annotation_colors = annotation_colors, annotation_legend = annotation_legend, main = main, fontsize = fontsize, fontsize_row = fontsize_row, fontsize_col = fontsize_col, fmat = fmat, fontsize_number = fontsize_number, ...)
	  garbage<-dev.off()
	  invisible(list(tree_row = tree_row, tree_col = tree_col, kmeans = km))

	}


subplot <- function(fun, x, y=NULL, size=c(1,1), vadj=0.5, hadj=0.5,
                    inset=c(0,0), type=c('plt','fig'), pars=NULL){

#  old.par <- par(no.readonly=TRUE)

    type <- match.arg(type)
    old.par <- par( c(type, 'usr', names(pars) ) )
    on.exit(par(old.par))

  if(missing(x)) x <- locator(2)

  if(is.character(x)) {
      if(length(inset) == 1) inset <- rep(inset,2)
      x.char <- x
      tmp <- par('usr')
      x <- (tmp[1]+tmp[2])/2
      y <- (tmp[3]+tmp[4])/2

      if( length(grep('left',x.char, ignore.case=TRUE))) {
          x <- tmp[1] + inset[1]*(tmp[2]-tmp[1])
          if(missing(hadj)) hadj <- 0
      }
      if( length(grep('right',x.char, ignore.case=TRUE))) {
          x <- tmp[2] - inset[1]*(tmp[2]-tmp[1])
          if(missing(hadj)) hadj <- 1
      }
      if( length(grep('top',x.char, ignore.case=TRUE))) {
          y <- tmp[4] - inset[2]*(tmp[4]-tmp[3])
          if(missing(vadj)) vadj <- 1
      }
      if( length(grep('bottom',x.char, ignore.case=TRUE))) {
          y <- tmp[3] + inset[2]*(tmp[4]-tmp[3])
          if(missing(vadj)) vadj <- 0
      }
  }

  xy <- xy.coords(x,y)

  if(length(xy$x) != 2){
    pin <- par('pin')
 #   tmp <- cnvrt.coords(xy$x[1],xy$y[1],'usr')$plt
    tmpx <- grconvertX( xy$x[1], to='npc' )
    tmpy <- grconvertY( xy$y[1], to='npc' )

    x <- c( tmpx - hadj*size[1]/pin[1],
            tmpx + (1-hadj)*size[1]/pin[1] )
    y <- c( tmpy - vadj*size[2]/pin[2],
            tmpy + (1-vadj)*size[2]/pin[2] )

 #   xy <- cnvrt.coords(x,y,'plt')$fig
    xyx <- grconvertX(x, from='npc', to='nfc')
    xyy <- grconvertY(y, from='npc', to='nfc')
  } else {
#    xy <- cnvrt.coords(xy,,'usr')$fig
      xyx <- grconvertX(x, to='nfc')
      xyy <- grconvertY(y, to='nfc')
  }

  par(pars)
  if(type=='fig'){
      par(fig=c(xyx,xyy), new=TRUE)
  } else {
      par(plt=c(xyx,xyy), new=TRUE)
  }
  fun
  tmp.par <- par(no.readonly=TRUE)

  return(invisible(tmp.par))
}



filename1 <- "%s"
output <- "%s/summary_%s_%s.cumulative"
cutoff <- 0.05
undetfound=%s
d1<-read.table(filename1, header=TRUE)
d1$sumcol=d1$proportion_of_reads

#d\$sumcol=d\$sumcol+d\$proportion_of_reads
sum=0

d1$ideal=1
d1$ideal[nrow(d1)]=0
for(i in 1:nrow(d1)){
sum=sum+d1$proportion_of_reads[i]
d1$sumcol[i]=1-sum}

cl=colorRampPalette(brewer.pal(12,"Paired"))(%s-undetfound)

n_samples=%s
if(n_samples>50){
	h_increase=n_samples/18		
		} else{
	h_increase=0}

pdf( paste(output,'.pdf', sep = ''), width = 11, height=7+h_increase)
par(mar=c(6,6,6,15) + 0.1, oma=c(h_increase*4,0,0,0), mgp = c(3, 1, 0))
plot(x=d1$read_length, y=d1$sumcol, ylim=c(0,1), panel.first = abline(h=seq(0.0,1,0.2), lty=1, col='grey'),type='l', pty="s", xlab=paste('Length of longest contiguous read segments with quality better than',cutoff),col.lab=rgb(0,0.5,0), ylab='proportion of reads',col.lab=rgb(0,0.5,0), lwd=2, col=cl[1], las=1)
lines(d1$read_length,d1$ideal, type='l', lty=3, col='black', lwd=2)


Title=tail(strsplit(strsplit(filename1, '.fastq.segments')[[1]][1],'/')[[1]],1)
title(paste('Summary for %s_%s'))
mtext(paste('p cutoff = ',cutoff), 3, line=1)
\n"""%(file1,path,groupname, readname,undetfound,n,n,groupname, readname.upper()))
	rscript.close()

def initcycle(n):

	rscript=open('%s/rtemp.R'%path,'a')
	rscript.write("""

for (i in 2:length(%s)){

                """%(n))

def moregraphs(filen, n, readname):

	rscript=open('%s/rtemp.R'%path,'a')
	rscript.write("""

filename%s <- "%s"
cutoff <- 0.05

d%s<-read.table(filename%s, header=TRUE)
d%s$sumcol=d%s$proportion_of_reads

#d\$sumcol=d\$sumcol+d\$proportion_of_reads
sum=0
undet=0
d%s$ideal=1
d%s$ideal[nrow(d%s)]=0
for(i in 1:nrow(d%s)){
sum=sum+d%s$proportion_of_reads[i]
d%s$sumcol[i]=1-sum}  

undet=grepl('Undetermined', filename%s)
if(undet=='TRUE'){
undetfound=1
lines(x=d%s$read_length, y=d%s$sumcol, type='l', lty=4, lwd=2, col='black')    
}else{
lines(x=d%s$read_length, y=d%s$sumcol, type='l', lty=1, lwd=2, col=cl[%s])     }            
"""%(n,filen, n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n))
	rscript.close()



def closecycle():

	rscript=open('%s/rtemp.R'%path,'a')
	rscript.write("""
}
""")


def legend(allsamples):

	rscript=open('%s/rtemp.R'%path,'a')
	rscript.write("""
if(undetfound==1){
l=legend(x=(length(d1$read_length)+length(d1$read_length)/10)-2, y=1.200, xpd=NA,c(%s "Undetermined", "Ideal"), lty=c(rep(1,%s),4,3), inset=c(-0.2,0), cex=0.5, col=c(cl,"black", "black"), lwd=2)}else{
l=legend(x=(length(d1$read_length)+length(d1$read_length)/10)-2, y=1.200, xpd=NA,c(%s "Ideal"), lty=c(rep(1,%s),3), inset=c(-0.2,0), cex=0.5, col=c(cl, "black"), lwd=2)
}
    """%(allsamples, len(allsamples.split()),allsamples, len(allsamples.split())))


def matrix(n, read_id, undetfound):
	m=n
	rscript=open('%s/rtemp.R'%path,'a')
	rscript.write("limit=length(d1$sumcol)-2\n")
	rscript.write("dmat=t(cbind(d1$sumcol[0:limit]") 
	if undetfound==1:
		n=n-1
	if n>1:
		for i in range(2,n):
			rscript.write(",d%s$sumcol[0:limit]"%i)
		rscript.write(",d%s$sumcol[0:limit]"%n)
	
	rscript.write("))\n")
	
	rscript.write("mountain_legend=rbind(basename(filename1)")
	if undetfound==1:
		m=m-1
	if m>1:
		for i in range(2,m):
			rscript.write(",basename(filename%s)"%i)
		rscript.write(",basename(filename%s)"%m)
		
	rscript.write(")")
	rscript.write("""
mountain_legend=as.data.frame.matrix(mountain_legend)
mountain_legend$V1=gsub(".segments","", mountain_legend$V1, fixed = TRUE)
mountain_legend$New <- rowMeans(dmat)
mountain_legend$New=format(round(mountain_legend$New, 3), nsmall = 3)
row.names(dmat)<-paste(mountain_legend$New, mountain_legend$V1, sep="   ")
colnames(dmat)<-seq(1,limit)
dmat=sqrt(dmat^2)
mycol=colorRampPalette(topo.colors(10))
pheatmap(dmat, cellheight=10, cellwidth=10, cluster_rows=FALSE, filename=paste(output,'.matrix.pdf', sep=''), cluster_cols=FALSE, legend=TRUE, main='Summary matrix for %s', color=mycol(100), breaks=c(seq(0,1,0.01)))    
    """%read_id)







def closegraph():
	rscript=open('%s/rtemp.R'%path,'a')
	rscript.write("""
par(xpd=NA)
text(x=(length(d1$read_length)+length(d1$read_length)/10)-2, y=1.170-l$rect$h, "The boxplot shows the reads' yield per sample", cex=0.5, adj=c(0,1) )
\ngarbage<-dev.off()\n\n""")

def processreads(path, reads1, reads2, groupname, undetfound, fqpath):

	if reads1[0].split('/')[-1].startswith('Undetermined'):
		reads1.append(reads1.pop(0))
		reads2.append(reads2.pop(0))
	print "Analyzing all R1...."
	### READ1 ####
	#print "READ1"
	if len(reads1)>1:
		#print 'first ',reads1[0]

		basegraph(reads1[0], 'r1', groupname, len(reads1), undetfound)
		initcycle(len(reads1))
		for c in reads1[1:]:
			#print c
			n=reads1.index(c)+1
			#print n
			moregraphs(c, n, 'r1')
		closecycle()
		legendstring=''
		for sample in reads1:
			if not sample.split('/')[-1].startswith('Undetermined'):
				legendstring+='"%s", '%sample.split('/')[-1].split('.segments')[0]

		legend(legendstring)

	else:
		basegraph(reads1[0], 'r1', groupname, len(reads1), undetfound)
		legendstring='"%s", '%reads1[0].split('/')[-1].split('.segments')[0]
		legend(legendstring)


	if fqpath!='' and glob.glob('%s/*.fastq*'%fqpath):
		linecount_f=open('%s/temp_linecount.txt'%path,'w')
		for r in reads1:
			if not 'Undetermined' in r:
				#print 'wc -l %s/../../fQsequences/%s'%(path, r.split('/')[-1].strip('.segments'))
				if glob.glob('%s/*.gz'%fqpath)!=[]:

					lines=int(commands.getoutput('zgrep -Ec "$" %s/%s'%(fqpath, r.split('/')[-1].split('.segments')[0])).split()[0])/4

				else:
					lines=int(commands.getoutput('wc -l %s/%s'%(fqpath, r.split('/')[-1].split('.segments')[0])).split()[0])/4
				linecount_f.write(r.split('.segments')[0].split('/')[-1]+'\t'+str(lines)+'\n')
				#print r, lines
		linecount_f.close()
		minigraph(path, reads1)
	closegraph()
	matrix(len(reads1), 'R1', undetfound)
	os.system('Rscript %s/rtemp.R'%path)
	if debug==1:
		os.system('mv %s/rtemp.R %s/rtemp_R1.R'%(path,path))

	### READ 2 ####
	print "Analyzing all R2...."
	if len(reads2)!=0:

		if len(reads2)>1:
			#print 'second ',reads2[0]

			basegraph(reads2[0], 'r2', groupname, len(reads2), undetfound)
			initcycle(len(reads2))
			for c in reads2[1:]:
				#print c
				n=reads2.index(c)+1
				#print n
				moregraphs(c, n, 'r2')
			closecycle()
			legendstring=''
			for sample in reads2:
				if not sample.split('/')[-1].startswith('Undetermined'):	
					legendstring+='"%s", '%sample.split('/')[-1].split('.segments')[0]

			legend(legendstring)



		else:
			basegraph(reads2[0], 'r2', groupname, len(reads2), undetfound)
			legendstring='"%s", '%reads2[0].split('/')[-1].split('.segments')[0]
			legend(legendstring)


		if fqpath!='' and glob.glob('%s/*.fastq*'%fqpath):
			minigraph(path, reads2)
		closegraph()

		matrix(len(reads2), 'R2', undetfound)
		os.system('Rscript %s/rtemp.R'%path)    
		if debug==1:
			os.system('mv %s/rtemp.R %s/rtemp_R2.R'%(path,path))

if __name__ == '__main__':

	path=''
	fqpath=''
	samplename='n'
	locus='n'
	undetfound=0
	debug=0
	opts, args = getopt.getopt(sys.argv[1:],"hdp:f:", ["help", "path","fqdir", "debug"])
	exclude=[]
	for opt, arg in opts:

		if opt == '-h':
			print'''
    -p --path path
    -d --debug
    '''

		if opt in ("-p", "--path"):
			path=arg

		if opt in ("-f", "--fqdir"):
			fqpath=arg	    

		if opt in ("-d", "--debug"):
			debug=1


	if path=='':
		sys.exit('No path (-p) specified')


	reads1=glob.glob('%s/*_L00*_R1*fastq.segments'%path)
	reads2=glob.glob('%s/*_L00*_R2*fastq.segments'%path)
	reads1.sort(key=natural_keys)
	reads2.sort(key=natural_keys)
	for r in reads1:
		if r.split('/')[-1].startswith('Undetermined'):

			if reads1.index(r)!=len(reads1)-1:
				undet_pos=reads1.index(r)
				reads1.insert(len(reads1)-1, reads1.pop(undet_pos))
				if reads2!=[]:
					reads2.insert(len(reads2)-1, reads2.pop(undet_pos))	
			undetfound=1
			break
	processreads(path, reads1, reads2, 'all', undetfound, fqpath)
	if os.path.exists('%s/rtemp.R'%path):
		os.system('rm %s/rtemp.R'%path) 
	if os.path.exists('%s/summary'%path):
		os.system('rm -r %s/summary'%path)
	if os.path.exists('%s/temp_linecount.txt'%path) and debug!=1:
		os.system('rm -r %s/temp_linecount.txt'%path)
	if os.path.exists('%s/Rplots.pdf'%path):
		os.system('rm -r %s/Rplots.pdf'%path)
	if os.path.exists('Rplots.pdf'):
		os.system('rm -r Rplots.pdf')
	os.system('mkdir %s/summary ; mv %s/summary_* %s/summary'%(path, path, path))
