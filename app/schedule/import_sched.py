import xlrd
import re
import datetime
import calendar
from dateutil.parser import parse
from app import db
from app.models import Workday


def import_schedule(schedule):
  day_index = []
  end_index = []

  with xlrd.open_workbook(schedule) as wb:
    cs = wb.sheet_by_index(0)
    num_cols = cs.ncols
    num_rows = cs.nrows

    for row_index in range(0, num_rows):
      for col_index in range(0, num_cols):
        cell_val = cs.cell(row_index, col_index).value
        if 'monday' in cell_val.lower():
          day_index.append((row_index, col_index))
        if 'floater' in cell_val.lower():
          if not end_index:
            end_index.append((row_index, col_index))
          else:
            if row_index not in end_index[0] and len(end_index) == 1:
              end_index.append((row_index, col_index))

  day_indices = []
  for i in day_index:
      for j in range(2, 10, 2):
        day_indices.append((i[0], (i[1] + j)))

  day_indices.insert(0, day_index[0])
  day_indices.insert(5, day_index[1])

  end_indices = []
  for i in end_index:
    for j in range(2, 10, 2):
      end_indices.append((i[0], (i[1] + j)))

  end_indices.insert(0, end_index[0])
  end_indices.insert(5, end_index[1])


  days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
  pattern = re.compile('^.*(?P<WD>Monday|Tuesday|Wednesday|Thursday|Friday?).*(?P<M>Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:tember|t)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s*(?P<D>\d*).*$', re.I)
  year = datetime.datetime.now().date().strftime("%Y")

  index = 0
  for x, y in day_indices:
    data_list = []
    for i in range(day_indices[index][0], (end_indices[index][0] + 1)):
      cell1, cell2 = cs.cell(i, y).value, cs.cell(i, y+1).value
      if i == day_indices[index][0]:
        day_cell = pattern.match(cell1)
        str_date = day_cell.group('M') + str(day_cell.group('D'))
        parsed_date = parse(str_date)
        weekday = day_cell.group('WD')
      elif cell1 == '': # ignore empty cells
        pass
      else: # stick everything else in data
        combined_cells = '{:<22} {}'.format(cell1, cell2)
        data_list.append(combined_cells)
        data_string = '\n'.join([data for data in data_list])
    
        workday = Workday(weekday=weekday,
                      date=parsed_date,
                      data=data_string)
        
        db.session.add(workday)
        db.session.commit()

    index += 1
  
