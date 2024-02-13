import tvdb_v4_official
import json
import sys
import os


apikey = "202a4721-032a-4ddd-b885-3a6d1aa6d5f8"
tvdb = tvdb_v4_official.TVDB(apikey)

searchTerm = sys.argv[1]


def search(searchTerm):
    searchTerm = str(searchTerm)
    searchData = tvdb.search(searchTerm)

    searchItems = []
    searchItemInfo = {}
    for searchItem in searchData:
        firstAirTime = None
        year = None
        searchItemInfo["name"] = searchItem["name"]
        searchItemInfo["id"] = searchItem["tvdb_id"]
        firstAirTime = searchItem.get("first_air_time")
        year = searchItem.get("year")

        if firstAirTime:
            searchItemInfo["year"] = firstAirTime
        elif year:
            searchItemInfo["year"] = year
        else:
            searchItemInfo["Year"] = "None"
        
        searchItems.append(searchItemInfo.copy())
    
    return searchItems


def getSeasonEpisodeList(seriesid, seasonnum):
    series = tvdb.get_series_extended(seriesid)

    for season in sorted(series["seasons"], key=lambda x: (x["type"]["name"], x["number"])):
        if season["type"]["name"] == "Aired Order" and season["number"] == seasonnum:
            season = tvdb.get_season_extended(season["id"])
            break
    else:
        season = None
    if season is not None:
        episodeList = []
        episodeInfo = {}
        for episode in season["episodes"]:
            episodeInfo["name"] = (episode["name"])
            episodeInfo["year"] = (episode["year"])

            episodeList.append(episodeInfo.copy())
        
        return episodeList


def getFilesInFolder(folder):
    mkvFiles = []
    for item in os.listdir(folder):
        mkvFiles.append(os.path.join(folder, item))

    mkvFiles.sort(key=os.path.getctime)

    if mkvFiles:
        return mkvFiles
    else:
        print("Folder is empty")
        return None


def makeEpisodeName(showName, episodeYear, seasonNumber, episodeNumber, episodeTitle):
    episodeName = f"{showName} ({episodeYear}) - S{seasonNumber:02d}E{episodeNumber:02d} - {episodeTitle}"
    return episodeName


def renameFile(old_path, new_path):
    try:
        os.rename(old_path, new_path)
        print(f"Renamed {old_path} to /n {new_path}")
    except OSError as e:
        print(f"Error renaming {old_path}: {e}")


def main():
    # Searching
    searchData = search(searchTerm)
    for x, item in enumerate(searchData):
        print(x, "|", item["name"], item["year"])

    # Selecting Show
    showSelection = int(input("What show are you looking for?: "))
    showid = searchData[showSelection]["id"]
    showName = searchData[showSelection]["name"]

    # Selecting Show Season Number
    seasonnumber = int(input("What season would you like to get?: "))

    episodeList = getSeasonEpisodeList(showid, seasonnumber)

    # Setting path where files are located
    destinationFolder = input("What is the destination path?: ")

    filesToRename = getFilesInFolder(destinationFolder)

    startingIndex = int(input("What episode index would you like to start on? (0 if none): "))

    for i, file in enumerate(filesToRename):
        episodeNumber = i + 1
        newName = makeEpisodeName(
            showName,
            episodeList[i+startingIndex]["year"],
            seasonnumber,
            episodeNumber + startingIndex,
            episodeList[i+startingIndex]["name"]
            )
        
        # Get the file extension
        _, file_extension = os.path.splitext(file)

        newFileName = f"{newName}{file_extension}"
        newFilePath = os.path.join(destinationFolder, newFileName)

        try:
            renameFile(file, newFilePath)
        except Exception as e:
            print(f"Error renaming file: {e}")


if __name__ == "__main__":
    main()
