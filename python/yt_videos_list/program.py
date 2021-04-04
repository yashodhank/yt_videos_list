import os
import datetime
from .     import file
from .notifications import Common
from .custom_logger import log
def determine_action(url, driver, scroll_pause_time, reverse_chronological, file_name, txt, csv, markdown, logging_locations):
 common_message = Common()
 now = datetime.datetime.now
 txt_exists = os.path.isfile(f'{file_name}.txt') if txt else False
 csv_exists = os.path.isfile(f'{file_name}.csv') if csv else False
 md_exists = os.path.isfile(f'{file_name}.md')  if markdown else False
 txt_videos = None
 csv_videos = None
 md_videos = None
 current_condition = (txt, txt_exists, csv, csv_exists, markdown, md_exists)
 update_conditions = set(
  (
   (True,  True,  True,  True,  True,  True),
   (True,  True,  True,  True,  False, False),
   (True,  True,  False, False, True,  True),
   (False, False, True,  True,  True,  True),
   (True,  True,  False, False, False, False),
   (False, False, False, False, True,  True),
   (False, False, True,  True,  False, False),
  )
 )
 if current_condition in update_conditions: videos_list, txt_videos, csv_videos, md_videos = file.scroller.scroll_to_old_videos(url, driver, scroll_pause_time, logging_locations, file_name, txt_exists, csv_exists, md_exists)
 else:           videos_list = file.scroller.scroll_to_bottom (url, driver, scroll_pause_time, logging_locations)
 if len(videos_list) == 0:
  log(common_message.no_videos_found, logging_locations)
  return
 if txt:
  if txt_exists: file.write.update_file('txt', videos_list, file_name, reverse_chronological, logging_locations, timestamp=now().isoformat().replace(':', '-').replace('.', '_'), stored_in_file=txt_videos)
  else:    file.write.create_file('txt', videos_list, file_name, reverse_chronological, logging_locations, timestamp=now().isoformat().replace(':', '-').replace('.', '_'))
 if csv:
  if csv_exists: file.write.update_file('csv', videos_list, file_name, reverse_chronological, logging_locations, timestamp=now().isoformat().replace(':', '-').replace('.', '_'), stored_in_file=csv_videos)
  else:    file.write.create_file('csv', videos_list, file_name, reverse_chronological, logging_locations, timestamp=now().isoformat().replace(':', '-').replace('.', '_'))
 if markdown:
  if md_exists:  file.write.update_file('md', videos_list, file_name, reverse_chronological, logging_locations, timestamp=now().isoformat().replace(':', '-').replace('.', '_'), stored_in_file=md_videos)
  else:    file.write.create_file('md', videos_list, file_name, reverse_chronological, logging_locations, timestamp=now().isoformat().replace(':', '-').replace('.', '_'))
