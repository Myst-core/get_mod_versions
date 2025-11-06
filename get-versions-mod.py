import requests
import json
import os

def get_file_from_folder():
  # lists files within folder 'modlist'
  files = os.listdir('modlist')

  # checks for only one file in folder
  if len(files) > 1:
    print('There is more than one file in this folder.\nPlease make sure there is only one file.')
  else:
    return files[0]

def get_mod_id(line):
  # removes unwanted whitespace
  line = line.strip()

  # check if the mod comes from modrinth
  if 'modrinth' not in line:
    print('This program can only check mod from modrinth.\nMake sure there are no mods from other websites.')
    return None, None
  
  else:
    # gets last 8 char from line
    mod_id = line[-8:]

    return mod_id, line

def main():
  # deletes output file if it exists already
  # > would append to the end of the file if this wasn't here
  if os.path.exists("mod_list.txt"):
    os.remove("mod_list.txt")

  filename = get_file_from_folder()

  # opens slug file
  with open(f'modlist/{filename}') as slugs:
    # loops through each line in file
    for i in slugs:

      mod_id, line = get_mod_id(i)

      # ends program if found that mod was not from modrinth
      if mod_id == None or line == None:
        break

      # selects mod using modrinth API url
      url = f"https://api.modrinth.com/v2/project/{mod_id}"
      resp = requests.get(url)
      status = resp.status_code
      
      # checks if mod exists
      if status == 404:
        print(line)
        print('Mod not found')
        break

      else:
        # gets data from selected mod
        data = resp.text
        
        # turns data into py json
        parse_json = json.loads(data)

        # gets specific data from the total
        project_id = parse_json['id']
        project_slug = parse_json['slug']
        game_versions = parse_json['game_versions']

        # filters for common strings in data:
        filtered_versions = [x for x in game_versions if '1.21' in x] # 1.21.x version
        filtered_versions = [x for x in filtered_versions if not '-' in x] # not a pre-release | '-' is common
        filtered_versions = [x for x in filtered_versions if not 'w' in x] # not a snapshot | 'w' is common

        # joins them into a readable string
        game_versions = ', '.join(filtered_versions)

        # opens / creates file for data
        # writes data to file
        with open('mod_list.txt', 'a') as f:
          f.write(project_id+'+')
          f.write(project_slug+'+')
          f.write(game_versions)
          f.write('\n')
          f.close()
    slugs.close()

main()