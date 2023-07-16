from z3 import *

def to_wat():
	# from chall.js
	binary = [0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 3, 2, 1, 0, 7, 9, 1, 5, 99, 104, 101, 99, 107, 0, 0, 10, 220, 7, 1, 217, 7, 0, 65, 0, 65, 0, 106, 65, 63, 113, 65, 2, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 57, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 29, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 63, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 44, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 53, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 42, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 45, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 43, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 42, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 35, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 37, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 62, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 28, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 36, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 56, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 59, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 60, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 35, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 39, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 40, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 60, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 50, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 50, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 50, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 20, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 61, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 32, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 38, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 40, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 47, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 42, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 43, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 31, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 37, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 24, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 28, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 24, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 19, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 49, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 33, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 55, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 38, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 62, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 48, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 39, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 53, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 38, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 20, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 33, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 42, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 3, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 40, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 0, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 7, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 35, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 45, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 35, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 62, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 46, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 20, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 44, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 55, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 33, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 1, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 37, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 2, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 4, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 43, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 47, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 29, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 26, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 32, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 19, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 32, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 52, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 47, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 42, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 53, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 31, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 47, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 0, 71, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 11]
	with open("out.wasm", 'wb') as f:
		for i in binary:
			f.write(i.to_bytes())

def get_lhs():
	# from chall.js
	rep = [[566, 843], [159, 238], [579, 643], [225, 557], [137, 293], [447, 533], [832, 863], [62, 808], [269, 546], [271, 390], [720, 733], [161, 753], [280, 876], [203, 700], [599, 645], [744, 885], [170, 227], [214, 766], [326, 797], [181, 315], [357, 920], [258, 403], [335, 854], [480, 687], [544, 755], [126, 777], [456], [467, 590], [115, 656], [104, 513], [401, 667], [249, 621], [799, 874], [445, 502], [577, 722], [665, 909], [304, 764], [40, 434], [368, 425], [324, 865], [49, 205], [392, 489], [731, 788], [260, 676], [313, 711], [469, 610], [139, 830], [689, 896], [38, 194, 929], [381], [414, 742], [71, 370], [84, 236], [379, 535], [522, 678], [117, 819], [247, 887], [291, 524], [698, 821], [491, 786], [412, 634], [423, 612], [73, 93], [51, 918], [216, 588], [95, 500], [150, 346], [192, 601], [148, 458], [282, 302], [511, 810], [359, 852], [709, 898], [555, 568], [82, 183], [60, 436], [337, 907], [348, 478], [172, 654], [128, 841], [106, 632], [623, 775]]
	offset = 37
	scale = 11
	# map character in flag -> which equations it is in
	m = []
	for positions in rep:
		inds = []
		for position in positions:
			inds.append((position - offset) // scale)
		m.append(inds)

	# map equation -> which characters in flag
	lhs = [[] for _ in range(82)]
	for i in range(len(m)):
		for equation_ind in m[i]:
			lhs[equation_ind].append(i)
	
	return(lhs)

def get_rhs():
	# from chall.js
	binary = [0, 97, 115, 109, 1, 0, 0, 0, 1, 5, 1, 96, 0, 1, 127, 3, 2, 1, 0, 7, 9, 1, 5, 99, 104, 101, 99, 107, 0, 0, 10, 220, 7, 1, 217, 7, 0, 65, 0, 65, 0, 106, 65, 63, 113, 65, 2, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 57, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 29, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 63, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 44, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 53, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 42, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 45, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 43, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 42, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 35, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 37, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 62, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 28, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 36, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 56, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 59, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 60, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 35, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 39, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 40, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 60, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 50, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 50, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 50, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 20, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 61, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 32, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 38, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 40, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 47, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 42, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 43, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 31, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 37, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 24, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 28, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 24, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 19, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 49, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 33, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 55, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 38, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 62, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 48, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 39, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 53, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 38, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 20, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 33, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 42, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 3, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 40, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 0, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 7, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 35, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 45, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 35, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 62, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 46, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 20, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 44, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 55, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 33, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 1, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 37, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 2, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 4, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 43, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 47, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 29, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 26, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 32, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 19, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 32, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 52, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 47, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 42, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 53, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 31, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 47, 71, 65, 0, 65, 0, 106, 65, 63, 113, 65, 0, 71, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 11]
	offset = 46
	scale = 11
	rhs = []
	for i in range(82):
		rhs.append(binary[offset + scale * i])
	return(rhs)

def get_code_for_z3():
	lhss = get_lhs()
	rhss = get_rhs()
	var = ' '.join(["x{}".format(x) for x in range(82)])
	var_comma = ', '.join(["x{}".format(x) for x in range(82)])
	print(var)
	print(var_comma)
	for i in range(82):
		lhs = lhss[i]
		rhs = rhss[i]
		if (len(lhs) == 2):
			s = "s.add((x{:02} + x{:02}) % 64 == {})".format(lhs[0], lhs[1], rhs)
		else:
			s = "s.add(x{:02} % 64 == {})".format(lhs[0], rhs)
		print(s)

def solve():
	# from get_code_for_z3()
	x00, x01, x02, x03, x04, x05, x06, x07, x08, x09, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31, x32, x33, x34, x35, x36, x37, x38, x39, x40, x41, x42, x43, x44, x45, x46, x47, x48, x49, x50, x51, x52, x53, x54, x55, x56, x57, x58, x59, x60, x61, x62, x63, x64, x65, x66, x67, x68, x69, x70, x71, x72, x73, x74, x75, x76, x77, x78, x79, x80, x81 = Ints('x00 x01 x02 x03 x04 x05 x06 x07 x08 x09 x10 x11 x12 x13 x14 x15 x16 x17 x18 x19 x20 x21 x22 x23 x24 x25 x26 x27 x28 x29 x30 x31 x32 x33 x34 x35 x36 x37 x38 x39 x40 x41 x42 x43 x44 x45 x46 x47 x48 x49 x50 x51 x52 x53 x54 x55 x56 x57 x58 x59 x60 x61 x62 x63 x64 x65 x66 x67 x68 x69 x70 x71 x72 x73 x74 x75 x76 x77 x78 x79 x80 x81')
	s = Solver()
	s.add((x37 + x48) % 64 == 2)
	s.add((x40 + x63) % 64 == 57)
	s.add((x07 + x75) % 64 == 29)
	s.add((x51 + x62) % 64 == 63)
	s.add((x52 + x74) % 64 == 44)
	s.add((x62 + x65) % 64 == 53)
	s.add((x29 + x80) % 64 == 42)
	s.add((x28 + x55) % 64 == 45)
	s.add((x25 + x79) % 64 == 43)
	s.add((x04 + x46) % 64 == 42)
	s.add((x66 + x68) % 64 == 35)
	s.add((x01 + x11) % 64 == 37)
	s.add((x16 + x78) % 64 == 62)
	s.add((x19 + x74) % 64 == 28)
	s.add((x48 + x67) % 64 == 36)
	s.add((x13 + x40) % 64 == 56)
	s.add((x17 + x64) % 64 == 59)
	s.add((x03 + x16) % 64 == 60)
	s.add((x01 + x52) % 64 == 35)
	s.add((x31 + x56) % 64 == 39)
	s.add((x21 + x43) % 64 == 40)
	s.add((x08 + x09) % 64 == 60)
	s.add((x12 + x69) % 64 == 50)
	s.add((x04 + x57) % 64 == 50)
	s.add((x36 + x69) % 64 == 50)
	s.add((x19 + x44) % 64 == 20)
	s.add((x18 + x39) % 64 == 61)
	s.add((x22 + x76) % 64 == 32)
	s.add((x66 + x77) % 64 == 38)
	s.add((x20 + x71) % 64 == 40)
	s.add((x38 + x51) % 64 == 47)
	s.add((x49 + x53) % 64 == 42)
	s.add((x09 + x41) % 64 == 43)
	s.add((x21 + x30) % 64 == 31)
	s.add((x50 + x60) % 64 == 37)
	s.add((x38 + x61) % 64 == 24)
	s.add((x37 + x75) % 64 == 28)
	s.add((x05 + x33) % 64 == 24)
	s.add((x26 + x68) % 64 == 19)
	s.add((x27 + x45) % 64 == 49)
	s.add((x23 + x77) % 64 == 33)
	s.add((x41 + x59) % 64 == 55)
	s.add((x33 + x65) % 64 == 38)
	s.add((x29 + x70) % 64 == 62)
	s.add((x54 + x57) % 64 == 48)
	s.add((x05 + x53) % 64 == 39)
	s.add((x08 + x24) % 64 == 53)
	s.add((x03 + x73) % 64 == 38)
	s.add((x00 + x73) % 64 == 20)
	s.add((x02 + x34) % 64 == 33)
	s.add((x27 + x64) % 64 == 42)
	s.add((x14 + x67) % 64 == 3)
	s.add((x45 + x61) % 64 == 40)
	s.add((x31 + x81) % 64 == 0)
	s.add((x60 + x80) % 64 == 7)
	s.add((x02 + x14) % 64 == 35)
	s.add((x28 + x78) % 64 == 45)
	s.add((x30 + x35) % 64 == 35)
	s.add((x43 + x54) % 64 == 62)
	s.add((x23 + x47) % 64 == 46)
	s.add((x13 + x58) % 64 == 20)
	s.add((x44 + x72) % 64 == 44)
	s.add((x10 + x34) % 64 == 55)
	s.add((x10 + x42) % 64 == 33)
	s.add((x15 + x50) % 64 == 1)
	s.add((x11 + x24) % 64 == 37)
	s.add((x17 + x36) % 64 == 2)
	s.add((x25 + x81) % 64 == 4)
	s.add((x42 + x59) % 64 == 43)
	s.add((x18 + x32) % 64 == 47)
	s.add((x07 + x70) % 64 == 29)
	s.add((x55 + x58) % 64 == 26)
	s.add((x06 + x46) % 64 == 32)
	s.add((x00 + x79) % 64 == 19)
	s.add((x22 + x71) % 64 == 32)
	s.add((x06 + x39) % 64 == 52)
	s.add((x12 + x32) % 64 == 47)
	s.add((x15 + x56) % 64 == 42)
	s.add((x47 + x72) % 64 == 53)
	s.add((x35 + x76) % 64 == 31)
	s.add((x20 + x63) % 64 == 47)
	s.add(x48 % 64 == 0)
	s.check()
	m = s.model()
	#https://stackoverflow.com/questions/70529941/z3-python-ordering-models-and-accessing-their-elements
	nicer = sorted([(d, m[d]) for d in m], key = lambda x: str(x[0])) 
	dic = "abcdefghijklmnopqrstuvwxyz0123456789_{}"
	flag = "".join([dic[int(str(x)) % 64] for (_, x) in nicer])
	print(flag)

solve()
