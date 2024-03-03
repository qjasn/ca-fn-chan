flet pack ./main.py \
  --product-name "算方阐" \
  --product-version "beta-0.1.0" \
  --copyright "CaFnChan Copyright (C) 2024 asahi_qin 秦奥楠" \
  --icon ./assets/icon.jpg
mv ./dist/main ./dist/ca-fn-chan
mv ./dist/main.app ./dist/ca-fn-chan.app
bash ./clean_build.sh