Changelog
=========
1.0.2 (2023-11-28)
- MVP version of the plugin

1.0.3 (2023-11-30)
- Fixed binding / product group item info sync from Amazon API
- Added different text label for 'Prime Videos' type items
- Added translations
- Added amplitude events

1.0.4 (2023-12-07)
- Added feature to overwrite title and description
- Added feature to limit title, description and description items

1.0.5 (2024-01-09)
- Lists functionality
- Table list page in admin

1.0.6 (2024-01-10)
- Multiple products selector in lists view
- Fatal error fix on plugin first install

1.0.7 (2024-01-24)
- Table creation and edit in admin added
- Added table selector in gutenberg block
- UI fixes

1.0.8 (2024-01-30)
- Scheduled job for product update in DB
- Internal testing UI fixes

1.0.9 (2024-02-08)
- Removed 'Reconnect' dropdown option from Amazon API status card
- Responsive fixes
- Affiliate dashboard URL corrections
- Amazon connected to display corrections (display name -> partner id)
- Site editor incompatibility message added
- UI changes to table creation/edit view
- Translations

1.1.0 (2024-02-12)
- Added option for surveys when any affiliate post is published
- Translations update

1.1.1 (2024-02-12)
- Temporary rest api url fix to bypass cache

1.1.2 (2024-02-12)
- Fixed cache issues

1.1.3 (2024-03-07)
- Added scrollbar to dropdown list component
- Added pre-defined row options in table creation process
- Block render style fixes
- Fixed table row option deletion issue
- Fixed PHP notices
- Added support for smaller screens when using product search modal
- Added feature to limit product title for table layout
- Amazon.com locale settings fix

1.1.4 (2024-03-12)
Fixed
- Rest API permissions check fix

1.1.5 (2024-03-18)
Fixed
- Removed product list fixed image height (crop issue)
- Fixed prime status inconsistency in search result modal
- Tutorial 2nd step asset change
- Intro step asset change
- Inherit block style from theme
- Description panel order changed
Added
- Product count validation in table create/edit view
- Pre-selected white color when adding product in table
- Description automatically enabled for single product and list with description layouts.

1.1.6 (2024-03-27)
Fixed
- Saving selected products on repeat search using search modal in multiple selection mode
- Prime status visual change
- Table view translations
Added
- Amazon dashboard CTA
- Added ASIN tooltip in product selector component

1.1.7 (2024-04-11)
Added
- PHP incompatibility notice

1.1.8 (2024-05-15)
Added
- Renamed Plugin to Hostinger Amazon Affiliate Connector

1.1.9 (2024-05-22)
Fixed
- Fixed simplified list mobile layout

2.0.0 (2024-06-04)
Added
- Menu management package

2.0.1 (2024-06-07)
Added
- Translations

2.0.2 (2024-06-26)
Refactored
- Amazon error code return messages
Added
- Added nl2br function for product description overwrite field
- Translations
Fixed
- Product thumbnail image overlap

2.0.3 (2024-07-04)
Fixed
- Missing table cells when some of the product information is missing
- Image aspect ratio on product list display type

2.0.4 (2024-07-10)
Added
- Plugin updates improvements

2.0.5 (2024-07-19)
Fixed
- Saving correct id in table collection

2.0.6 (2024-07-29)
Added
- Remove hpanel-mf-components library from project and replace it with hcomponents library

2.0.7 (2024-09-03)
Fixed
- Product update schedule

2.0.8 (2024-09-11)
- Update packages

2.0.9 (2024-09-12)
- Security update

2.0.10 (2024-09-23)
- Updated readme file

2.0.11 (2024-10-09)
- Main page header update: 1. Add title of the page; 2. Add tutorial explaining Amazon affiliate plugin

2.0.12 (2024-10-16)
- Aligned menu items with admin bar

2.0.13 (2024-11-13)
- Update hostinger packages

2.0.14 (2024-11-26)
- Keyless functionality

2.0.15 (2024-11-28)
- Changed plugin update url

2.0.16 (2024-12-13)
- Icon package update
- Duplicate API queries fix

2.0.17 (2024-12-17)
- Duplicate items fix
- Pricing fix using Scraper API

2.0.18 (2025-01-08)
- Table facelift
- Added preview website link in navbar

2.0.19 (2025-01-23)
- Fixed compatibility issue
- Fixed images in table view

2.0.20 (2025-01-27)
- Clean orphaned products on fetch
- Fixed images overflow in list view

2.0.21 (2025-01-29)
- Add tooltip popover for learn how to use plugin
- Fixed image overflow in search results
- Fixed duplicate products in search results
- Added inactive state for products
- Fixed copy table function

2.0.22 (2025-02-10)
- Fixed tld param for sg country code
- Fixed keyword list duplication
- Changed frequency of product update
- Fixed broken validation message

2.0.23 (2025-02-17)
- Improved table validation
- Added ability to choose localized Amazon locale when using API
- Fixed missing product descriptions when using keyless version

2.0.24 (2025-02-24)
- Added new amplitude events
- Fixed table search no results template
- Added missing translations

2.0.25 (2025-03-04)
- Refactored country params sent to proxy API
- Fixed title or description length validation in Gutenberg block
- Fixed missing products in table when more than 3
- Settings page improvements

2.0.26 (2025-03-05)
- Cronjob interval changes

2.0.27 (2025-03-11)
- Added source param to proxy API requests

2.0.28 (2025-03-17)
- Update with latest hcomponents version and color palette
