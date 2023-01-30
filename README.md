# pyguis

Guis for sql dbs, with support for reading images from http.

Uses [dearpygui](https://github.com/hoffstadt/DearPyGui).

## Arguments

[.] Input commandline args in ImGUI window, get output as yaml.

## urlimages

Dataframes with images

- [x] Show rows of images from urls.
- [x] Show/hide images.
- [x] Reload csv file.
- [x] Paginate.
- [ ] Dynamic textures.
- [ ] Load column data types from config.
- [ ] Layout rows with images and rest from config.
- [ ] Show/hide columns.
- [ ] Sort columns ( needs to be global ).
- [ ] Filter columns ( needs to be global ).
- [ ] Meta column with multiple images and switch.
- [ ] Comments and listboxes for rows.

```
┌─┬─────────────────────────────────────────────────────┬─┐
│ ├─────────────────────────────────────────────────────┤ │
│ │                                                     │ │
│ │ csv_file      base_url         [ ] images           │ │
│ │                                                     │ │
│ ├─────────────────────────────────────────────────────┤ │
│ ├─────────────────────────────────────────────────────┤ │
│ │   Columns                                           │ │
│ │                                                     │ │
│ ├─────────────────────────────────────────────────────┤ │
│ │                                                     │ │
│ │   Rows                                              │ │
│ │                                                     │ │
│ │                                                     │ │
│ │                                                     │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘

```

## Database/csv plots 

[ ] Given options to choose columns.
