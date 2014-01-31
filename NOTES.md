# Misc notes for future me / developers

## Single instance requires pip & tendo
	sudo apt-get install python-pip
	pip install tendo

## TV Shows (and maybe proper movie titles)

Disc info can be obtained, it returns a lot more information about each disc instead of just the 'is disc inserted'
```makemkvcon -r info disc:[index]```

## Strings returned:

### Drive scan messages

	DRV:index,visible,enabled,flags,drive name,disc name
	index - drive index
	visible - set to 1 if drive is present
	enabled - set to 1 if drive is accessible
	flags - media flags, see AP_DskFsFlagXXX in apdefs.h
	drive name - drive name string
	disc name - disc name string

### Disc information output messages

	TCOUT:count
	count - titles count

### Disc, title and stream information

	CINFO:id,code,value
	TINFO:id,code,value
	SINFO:id,code,value

	id - attribute id, see AP_ItemAttributeId in apdefs.h
	code - message code if attribute value is a constant string
	value - attribute value


#### Example

Title count

	TCOUNT:7

C = Disc info

	CINFO:1,6209,"Blu-ray disc"
	CINFO:2,0,"Breaking Bad: Season 1: Disc 1"
	CINFO:28,0,"eng"
	CINFO:29,0,"English"
	CINFO:30,0,"Breaking Bad: Season 1: Disc 1"
	CINFO:31,6119,"<b>Source information</b><br>"
	CINFO:32,0,"BREAKINGBADS1"
	CINFO:33,0,"0"

T = Title info

	TINFO:0,2,0,"Breaking Bad: Season 1: Disc 1"
	TINFO:0,8,0,"7"
	TINFO:0,9,0,"0:58:06"
	TINFO:0,10,0,"12.5 GB"
	TINFO:0,11,0,"13472686080"
	TINFO:0,16,0,"00763.mpls"
	TINFO:0,25,0,"1"
	TINFO:0,26,0,"262"
	TINFO:0,27,0,"Breaking_Bad_Season_1_Disc_1_t00.mkv"
	TINFO:0,28,0,"eng"
	TINFO:0,29,0,"English"
	TINFO:0,30,0,"Breaking Bad: Season 1: Disc 1 - 7 chapter(s) , 12.5 GB"
	TINFO:0,31,6120,"<b>Title information</b><br>"
	TINFO:0,33,0,"0"


	2 - Disc Title
	9 - Length of chapters
	10 - File size
	28 - audio short code
	29 - audio long code

## Perfered language

```CINFO``` provides title language, config this

	CINFO:28,0,"eng"
	CINFO:29,0,"English"
