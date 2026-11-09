param([string]$Name, [int]$Width = 1400, [string]$Kind = "image")
$s = $env:MUSE_MEDIA_DIR   # folder where muse2api saves outputs
$o = $env:REVIEW_DIR       # folder for review copies
New-Item -ItemType Directory -Force $o | Out-Null
if ($Kind -eq "video") {
  $f = Get-ChildItem $s -Filter *.mp4 | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  Copy-Item $f.FullName "$o\$Name.mp4" -Force
  ffmpeg -y -loglevel error -i "$o\$Name.mp4" -vf "fps=2.4,scale=240:-1,tile=8x3" -frames:v 1 "$o\$Name`_dense.png"
} else {
  $f = Get-ChildItem $s -File | Where-Object Extension -ne ".mp4" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  ffmpeg -y -loglevel error -i $f.FullName -vf "scale=$($Width):-1" "$o\$Name.png"
}
"$($f.Name) $($f.LastWriteTime)"
