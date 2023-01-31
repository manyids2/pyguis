# pyguis

Guis for sql dbs, with support for reading images from http.

Uses [dearpygui](https://dearpygui.readthedocs.io/en/latest/).

## Arguments

- [.] Input commandline args in ImGUI window, get output as yaml.

## urlimages

Dataframes with images

- [x] Show rows of images from urls.
- [x] Show/hide images.
- [x] Reload csv file.
- [x] Paginate.
- [x] Dynamic textures ( only load for those on page ).
- [x] Key for reload.
- [ ] Define widgets.
    - [x] layout
    - [x] settings - kinda
    - [ ] table ( paginated )
    - [ ] state ( debug )
- [ ] Show/hide columns.
- [ ] Sort columns ( needs to be global ).
- [ ] Filter columns ( needs to be global ).
- [ ] Load column data types from config.
- [ ] Layout rows with images and rest from config.
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

- [ ] Given options to choose columns.
