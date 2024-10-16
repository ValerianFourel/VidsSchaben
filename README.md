

In order to download the data we need to:

yt-dlp -i --flat-playlist --print-to-file "| %(upload_date)s | %(duration)s | %(view_count)s | %(like_count)s | %(title)s | %(id)s | %(webpage_url)s | %(description)s \_/" list_PamelaRf1_VideosSmallDataset.txt "https://www.youtube.com/@PamelaRf1"

python FromTxtmakeJson.py TextFilesOriginal/list_PamelaRf1_VideosSmallDataset.txt

Then you can process One Subject or Multiple subjects:

 python DatasetReductionOneYoutuber.json ProcessedJson/list_PamelaRf1_VideosSmallDataset_VideosObject.json

For multiple:

 python testAllDatasetsDatasetReduction.py ['Mins','Min','Minute','Minutes']


After this step we should obtain a json file ready to be used in downloading data:
python ScriptDownloadMulti.py --file_path /home/vfourel/ProjectGym/SmallDataset/downloadingReadyJsonAllDatasets/_PamelaRf1_VideosSmallDataset_VideosObject_matching_Download_ready.json \
  --base_download_dir /home/vfourel/ProjectGym/DownloadedOutputHighQuality
