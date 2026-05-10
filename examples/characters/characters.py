##############################################################
######################### Raw regex ########################## 
##############################################################
#
#  ((one|two|three|[369])|[!.])
#
##############################################################
########################### Engine ########################### 
##############################################################
#
#  Python
#
##############################################################
########################### Tests ############################ 
##############################################################
#
#  test 1:
#      pattern: 
#              asdasdsadasonesaagsdgs
#      match 1: 
#              one
#          group 1: 
#                  one
#          group 2: 
#                  one
#
#  test 2:
#      pattern: 
#              one two three
#      match 1: 
#              one
#          group 1: 
#                  one
#          group 2: 
#                  one
#
#  test 3:
#      pattern: 
#              two three
#      match 1: 
#              two
#          group 1: 
#                  two
#          group 2: 
#                  two
#
#  test 4:
#      pattern: 
#              three
#      match 1: 
#              three
#          group 1: 
#                  three
#          group 2: 
#                  three
#
#  test 5:
#      pattern: 
#              vxvcxv
#      No matches
#
#  test 6:
#      pattern: 
#              vxvcxv!
#      match 1: 
#              !
#          group 1: 
#                  !
#          group 2: 
#                  None
#
#  test 7:
#      pattern: 
#              vxvcxv.ad
#      match 1: 
#              .
#          group 1: 
#                  .
#          group 2: 
#                  None
#
#  test 8:
#      pattern: 
#              asd.
#      match 1: 
#              .
#          group 1: 
#                  .
#          group 2: 
#                  None
#
#  test 9:
#      pattern: 
#              144555
#      No matches
#
#  test 10:
#      pattern: 
#              1443
#      match 1: 
#              3
#          group 1: 
#                  3
#          group 2: 
#                  3
#
#  test 11:
#      pattern: 
#              54456
#      match 1: 
#              6
#          group 1: 
#                  6
#          group 2: 
#                  6
#
#  test 12:
#      pattern: 
#              9
#      match 1: 
#              9
#          group 1: 
#                  9
#          group 2: 
#                  9
#
##############################################################
####################### Generated code ####################### 
##############################################################
import re

text = ""   # empty
regex = '((one|two|three|[369])|[!.])'


match_object = re.search(
    regex, 
    text
)
