# speedFactor can be None or x30, x60, etc
def get_setpts(speedFactor):
    if speedFactor == 'None':
        return None
    else:
        speed = int(speedFactor[1:])
        setptsVal = 1.0 / int(speedFactor[1:])
        setptsStr = 'setpts=' + str(setptsVal) + '*PTS'
        return setptsStr

# example: fade=t=in:st=0:d=0.5
def get_fade_in(on, start, duration):
    if not on:
        return None
    else:
        filter = 'fade=t=in:st=' + str(start) + ':d=' + str(duration)
        return filter

# example: fade=t=out:st=45.177:d=0.5
def get_fade_out(on, start, duration):
    if not on:
        return None
    else:
        filter = 'fade=t=out:st=' + str(start) + ':d=' + str(duration)
        return filter

# filters = [] list of options
# e.g. ['setpts=0.0333*PTS', 'fade=t=in:st=0:d=0.5']
# where first element is for timelapse and second element is for fade in effect
def get_filters(filters):
  filtersStr = ''
  for filter in filters:
      if filter is not None:
          if len(filtersStr) > 0:
              filtersStr = filtersStr + ',' + filter
          else:
              filtersStr = filter
  return filtersStr
  
