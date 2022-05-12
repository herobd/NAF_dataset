# National Archives Forms Dataset

VERSION 3
* Printed text transcriptions added. These are from Tesseract. The test/valid set ones were hand corrected, but the train set was only hand corrected a little. They aren't very good results.
* A few more corrections

VERSION 2
* Corrections to various annotation errors.
* Test/Valid transcption added
* Train handwriting transcription added (though noisy)

This dataset was created with images provided by the United States National Archive and FamilySearch.

This was released (v1) in conjunction with the paper "Deep Visual Template-Free Form Parsing":
* Paper: http://arxiv.org/abs/1909.02576
* Code: https://github.com/herobd/Visual-Template-Free-Form-Parsing

Version 2 was used for "Visual FUDGE: Form Understanding via Graph Editing" http://arxiv.org/abs/2105.08194 (just the corrections, not the transcriptions).

Version 3 was used for "End-to-end Document Recognition and Understanding with Dessurt" https://arxiv.org/abs/2203.16618


![Annotated image from dataset](/ex_images/ex_dataset.png)

## Data distribution
THESE ARE NOT RIGHT FOR VERSION 2. But they should give you a good idea of what it looks like. The full dataset in v2 has 708 training, 75 validation, and 77 test set images.
![Data distriburion](/ex_images/naf_table.png)

"Simple" refers to the section of the data used in "Deep Visual Template-Free Form Parsing". FUDGE used all of it.

## Setup
1. Download `labeled_images.tar.gz` from the Github [release](https://github.com/herobd/NAF_dataset/releases/tag/v1.0) and put it in the dataset directory root.
2. Run: `./move_images.sh`  (This extracts the images and puts them in the right group directory.)

The configutation files for the "Deep Visual Template-Free Form Parsing" code expects this directory to be nested in a `data` directory at the same level as the repo directory.

i.e.
```
│
├─ data/
│  └─ NAF_dataset/
│     └─ labeled_images.tar.gz
└─ Visual-Template-Free-Form-Parsing/
```


## Information

I am releasing the images used with our paper "Deep Visual Template-Free Form Parsing," but there are more unlabeled images. If you are interested in using them, contact me: briandavis@byu.net


The goal of this data is to capture relationships between text/handwriting entities on form images.
The transcription GT has been partial added (printed text on the training set is missing). Unfortunately there isn't a plan to add any more.

The form images are organized into "groups", each group containing images of the same form type.
I tried to be picky in keeping forms seperate that contain even one different field, but it really is an estimate that was intended to speed up annotation.

The `groups` directory contains a directory for each group.
Within each group directory there are jpg and json files, which are linked by having the same file name (except for extension).

The tools used to annotate can be found here: <https://github.com/herobd/formlabeling.git>


The jsons have the following information:

* `imageFilename`: the image name this json corresponds to
* `width` & `height`: size of the original image (here for convienence)
* `fieldBBs` & `textBBs`: list of field/text bounding box objects
  * These objects have:
    * `poly_points`: list of [x,y] pairs, the box corners going top-left,top-right,bottom-right,bottom-left (they aren't restricted to be a rectangle!)
    * `type`: one of [`text`,`textP`,`textMinor`,`textInst`,`textNumber`,`fieldCircle`,`field`,`fieldP`,`fieldCheckBox`,`graphic`,`comment`,`fieldRegion`,`fieldCol`,`fieldRow`]
    * `id`: unique id that is either "f#" or "t#" depending if it is a field or text
    * `isBlank`: only for fields, has a number.
      * `0`: text
      * `1`: handwriting
      * `2`: print (or stamp)
      * `3`: blank
      * `4`: signature
* `pairs`: list of id tuples of relationships between text and field boxes
* `samePairs`: list of id tuples of relationships between text and text or field and field
* `transcriptions`: (NEW) dictionary of BB ids to their string transcription (see below for special characters).
* `actualPage_corners`: cordinates of phyisical page corners
* `page_corners`: cordinates of corners if the page where actually a polygon (e.g. not ripped corners)
* `horzLinks`: list of "horizontal lines", each horizontal line being a list of ids of boxes that all form a horizontal line not broken by dividing lines or gaps.



The types have the following meaning:
* `text`: Pre-printed text that is at most a few lines. May be a label is paired with a field.
* `textP`: Pre-printed text in a long paragraph, or a prose/fill-in-the-blank area.
* `textMinor`: A minor label. All nested labels are this type.
* `textInst`: Pre-printed instructions. Sometimes a minor label by position, but instruction in content.
* `textNumber`: A digit (or letter) that is part of an enumeration.
* `field`: A place where a respose is to be written/typed/stamped.
* `fieldP`: Blank in a prose/fill-in-the-blank area.
* `fieldCircle`: Pre-printed text that is intended to be marked (or left unmarked) with a circle or strike-through.
* `fieldCheckBox`: A checkbox, or simiar.
* `graphic`: An image, photograph, etc.
* `comment`: Any added writing or text which is not in a field.
* `fieldRegion`: Used if there are multiple documents in an image to denote the different images. Also done with repeated records.
* `fieldCol`: A column of a table, captures the entire column. Individual cells are not annotated.
* `fieldRow`: A row of a table.

Some special characters are used in the transcription:
* "«text»" indicates that "text" had a strikethrough
* "¿" indicates the transcriber could not read a character
* "§" indicates the whole line or word was illegible
* "" (empty string) is if the field was blank

## Citing

If you use this data, please cite our paper:
B. Davis, B. Morse, S. Cohen, B. Price, C. Tensmeyer, "Deep Visual Template-Free Form Parsing," in International Conference on Document Analysis and Recognition (ICDAR),  2019.
