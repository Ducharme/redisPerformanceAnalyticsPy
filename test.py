import numpy as np

#list indices must be integers or slices, not tuple

deviceId = 'test-36817591'
topic = 'topic_1'

streamArr = [
  #[dts, sts, wts, rts, seq]
  ['test-36817591', 1, 1650012179150, 1650012179164, 1650012179280, 1650012179286],
  ['test-36817591', 3, 1650012180152, 1650012180163, 1650012180291, 1650012180297],
  ['test-36817591', 5, 1650012181153, 1650012181164, 1650012181272, 1650012181278],
  ['test-36817591', 4, 1650012182154, 1650012182167, 1650012182273, 1650012182280],
  ['test-36817591', 7, 1650012183154, 1650012183170, 1650012183281, 1650012183287],
  ['test-36817591', 2, 1650012184154, 1650012184166, 1650012184266, 1650012184273],
  ['test-36817591', 6, 1650012185156, 1650012185167, 1650012185273, 1650012185275],
]
print (streamArr)

npArr = np.array(streamArr)
print (npArr)

sortedArr = npArr[npArr[:, 1].argsort()]
print (sortedArr)