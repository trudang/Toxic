import numpy as np

a = np.array([[0.0, 0.88930717193299691, 0.76311083145594005, 0.98537789291905831, 0.80182997810546019, 0.82975423825159578, 0.81304420436260272, 0.77874913546420799, 0.72816269791202515, 0.83093663280461316], [0.88930717193299691, 0.0, 0.74994634966272888, 1.0, 0.7889262326339751, 0.8800104304990084, 0.82835023494841609, 0.89389401110982003, 0.79071787509011993, 0.86973792534880057], [0.76311083145594294, 0.74994634966272888, 0.0, 0.860434351872434, 0.71850979429194473, 0.7515486692890555, 0.71906278223162934, 0.74486602696654136, 0.70108673831758006, 0.76691566338630579], [0.98537789291905831, 1.0, 0.860434351872434, 0.0, 0.93316709805307829, 0.97130983655496972, 0.9133810235902351, 0.78708647134585663, 0.81588842417949436, 0.8672973177255886], [0.80182997810546208, 0.7889262326339751, 0.71850979429194473, 0.93316709805307829, 0.0, 0.79493750147806685, 0.77494122448820546, 0.77121766616766207, 0.77277660874382281, 0.79970008506427659], [0.82975423825159578, 0.8800104304990084, 0.7515486692890555, 0.97130983655496872, 0.79493750147806874, 0.0, 0.80468669484986999, 0.76413622916701007, 0.71752826133969494, 0.81880502450062687], [0.81304420436260272, 0.82835023494841609, 0.71906278223162934, 0.9133810235902361, 0.77494122448820546, 0.80468669484986899, 0.0, 0.74783583397974285, 0.70723571213463632, 0.8025721790490864], [0.77874913546420799, 0.89389401110982003, 0.74486602696654136, 0.78708647134585663, 0.77121766616766207, 0.76413622916701007, 0.74783583397974285, 0.0, 0.65115379301553356, 0.82293544167789323], [0.72816269791202515, 0.79071787509011804, 0.70108673831757728, 0.81588842417949237, 0.77277660874382281, 0.71752826133969494, 0.70723571213463632, 0.65115379301553356, 0.0, 0.79933157174283631], [0.83093663280461227, 0.86973792534880057, 0.76691566338630579, 0.8672973177255886, 0.79970008506427659, 0.81880502450062687, 0.80257217904908829, 0.82293544167789323, 0.79933157174283542, 0.0]])

print a

# b = [[ 0.          0.8893072   0.76311082  0.98537791  0.80182999  0.82975423
#    0.81304419  0.77874911  0.72816271  0.83093661]
#  [ 0.8893072   0.          0.74994636  1.          0.78892624  0.88001043
#    0.82835025  0.89389402  0.7907179   0.86973792]
#  [ 0.76311082  0.74994636  0.          0.86043435  0.71850979  0.75154865
#    0.71906281  0.74486601  0.70108676  0.76691568]
#  [ 0.98537791  1.          0.86043435  0.          0.9331671   0.97130984
#    0.91338104  0.78708649  0.8158884   0.86729729]
#  [ 0.80182999  0.78892624  0.71850979  0.9331671   0.          0.79493749
#    0.77494121  0.77121764  0.7727766   0.79970008]
#  [ 0.82975423  0.88001043  0.75154865  0.97130984  0.79493749  0.
#    0.80468667  0.76413625  0.71752828  0.81880504]
#  [ 0.81304419  0.82835025  0.71906281  0.91338104  0.77494121  0.80468667
#    0.          0.74783581  0.70723569  0.80257219]
#  [ 0.77874911  0.89389402  0.74486601  0.78708649  0.77121764  0.76413625
#    0.74783581  0.          0.6511538   0.82293546]
#  [ 0.72816271  0.7907179   0.70108676  0.8158884   0.7727766   0.71752828
#    0.70723569  0.6511538   0.          0.79933155]
#  [ 0.83093661  0.86973792  0.76691568  0.86729729  0.79970008  0.81880504
#    0.80257219  0.82293546  0.79933155  0.        ]]

# print a == b