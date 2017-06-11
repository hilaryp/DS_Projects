# shapefiles: http://www.nyc.gov/html/dcp/html/bytes/districts_download_metadata.shtml#bcd
# ACS/PUMS data: http://www.census.gov/acs/www/data_documentation/pums_data/

library(ggplot2)
library(plyr)
require('gpclib')
library(maptools)
gpclibPermit()
library(scales)
library(rgdal)

# load ACS/PUMS 2010 & 2013 data, pull out relevant columns
d13 <- read.csv("ss13pny.csv")
d12 <- read.csv("ss12pny.csv")
d11 <- read.csv("ss11pny.csv")
d10 <- read.csv("ss10pny.csv")
d09 <- read.csv("ss09pny.csv")
d08 <- read.csv("ss08pny.csv")
d07 <- read.csv("ss07pny.csv")
d06 <- read.csv("ss06pny.csv")
d05 <- read.csv("ss05pny.csv")

df <- subset(d, select = c('SPORDER', 'PUMA', 'PWGTP', 'AGEP', 'ENG', 
                           'LANX', 'SEX', 'LANP'))

# c('SPORDER'='ID', 'PUMA'='PUMA', 'PWGTP'='Weight', 'AGEP'='Age', 'ENG'='EngFluency',
#   'LANX'='OtherLang', 'SEX'='Sex', 'LANP'='Language')

df$year <- rep(2013, nrow(df))
df2$year <- rep(2010, nrow(df2))
data <- rbind(df, df2)

# identify which PUMAs make up Manhattan, work with that subset for now
manhattan <- c(3801:3810)
nyc <- subset(data, PUMA %in% manhattan)

#bronx <- c(3701:3710)
#queens <- c(4101:4114)
#brooklyn <- c(4001:4018)
#staten <- c(3901:3903)

# Make language a factor so we can re-map it to names
nyc$LANP <- as.factor(nyc$LANP)
nyc$language <- revalue(as.factor(nyc$LANP), c('601'="Jamaican Creole", '602'="Krio", '607'="German",
                        '608'="Pennsylvania Dutch", '609'="Yiddish", '610'="Dutch",
                        '611'="Afrikaans", '614'="Swedish", '615'="Danish", '616'="Norwegian", 
                        '619'="Italian", '620'="French", '622'="Patois", '623'="French Creole", 
                        '624'="Cajun", '625'="Spanish", '629'="Portuguese", '631'="Romanian", 
                        '635'="Irish Gaelic", '637'="Greek", '638'="Albanian", '639'="Russian", 
                        '641'="Ukrainian", '642'="Czech", '645'="Polish", '646'="Slovak", 
                        '647'="Bulgarian", '648'="Macedonian", '649'="Serbo-Croatian", 
                        '650'="Croatian", '651'="Serbian", '653'="Lithuanian", '654'="Latvian", 
                        '655'="Armenian", '656'="Persian", '657'="Pashto", '658'="Kurdish", 
                        '662'="India N.E.C.", '663'="Hindi", '664'="Bengali", '665'="Panjabi", 
                        '666'="Marathi", '667'="Gujarati", '671'="Urdu", '674'="Nepali", 
                        '675'="Sindhi", '676'="Pakistan N.E.C.", '677'="Sinhalese", '679'="Finnish", 
                        '682'="Hungarian", '689'="Uighur", '691'="Turkish", '694'="Mongolian", 
                        '701'="Telugu", '702'="Kannada", '703'="Malayalam", '704'="Tamil", '708'="Chinese", 
                        '711'="Cantonese", '712'="Mandarin", '714'="Formosan", '717'="Burmese", 
                        '720'="Thai", '721'="Mien", '722'="Hmong", '723'="Japanese", '724'="Korean", 
                        '725'="Laotian", '726'="Mon-Khmer, Cambodian", '728'="Vietnamese", 
                        '732'="Indonesian", '739'="Malay", '742'="Tagalog", '743'="Bisayan", 
                        '744'="Sebuano", '746'="Ilocano", '750'="Micronesian", '752'="Chamorro", 
                        '761'="Trukese", '767'="Samoan", '768'="Tongan", '776'="Hawaiian", '777'="Arabic", 
                        '778'="Hebrew", '779'="Syriac", '780'="Amharic", '783'="Cushite", '791'="Swahili", 
                        '792'="Bantu", '793'="Mande", '794'="Fulani", '796'="Kru, Ibo, Yoruba", 
                        '799'="African", '806'="Other Algonquian", '819'="Ojibwa", 
                        '862'="Apache", '864'="Navajo", '907'="Dakota", '924'="Keres", 
                        '933'="Cherokee",  '964'="Zuni", '985'="Other Indo-European",  
                        '986'="Other Asian", '988'="Other Pacific Island",  
                        '989'="Other African", '990'="Aleut-Eskimo", 
                        '992'="South/Central American Indian",
                        '993'="Other North American Indian", 
                        '994'="Other", '996'="Not specified"))

# Get rid of rows with no other language (i.e., English-only)
man_data <- subset(nyc, language != 'NA')
# Get language counts per year by adding person weights
summary <- ddply(man_data, .(year, language, PUMA), summarize, count=sum(PWGTP))
summary$name <- revalue(summary$PUMA, c('3810'='SoHo', '3809'='LES', '3807'='Chelsea', 
                                        '3808'='Murray Hill', '3806'='UWS', '3805'='UES',
                                        '3802'='W. Harlem', '3803'='C. Harlem', 
                                        '3804'='E. Harlem', '3801'='Wash.Hts.'))
# The top three languages have so vastly many more speakers that we can't put
# them on the same plot as the others
big3 <- subset(summary, language %in% c('Spanish', 'Chinese', 'French'))
next5 <- subset(summary, language %in% c('Korean', 'German', 'Japanese', 'Cantonese', 
                                          'Russian'))
top10 <- subset(summary, language %in% c('Spanish', 'Chinese', 'French', 'Korean', 
                                         'German', 'Japanese', 'Cantonese', 
                                         'Russian', 'Hebrew', 'Italian'))

### Create first plot
# Adding lm but it's pretty meaningless with only two data points...
ggplot(top10, aes(year, count, color=language))+ 
  geom_point()+ 
  facet_grid(~name)+
  stat_smooth()+
  scale_y_log10()+
  theme_bw()+ 
  labs(title="Change in number of language speakers in Manhattan, 2005-2013", 
       x="\nAmerican Community Survey Year", 
       y="Log-Scaled Estimated Number of Speakers\n", 
       color="Language")

### Create second plot
# Read in community shapefile with correct projection
nyc_map <- readShapeSpatial("../nycd_14d/nycd", proj4string = CRS("+proj=lcc +lat_1=40.66666666666666 +lat_2=41.03333333333333 +lat_0=40.16666666666666 +lon_0=-74 +x_0=300000 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs "))
# Transform projection into something more standard...
nyc_map = spTransform(nyc_map, CRS("+proj=longlat +datum=WGS84"))
# Make shapefile into a ggplot-readable dataframe
nyc_map@data$id = rownames(nyc_map@data)
nyc_map.points = fortify(nyc_map, region="id")
nyc_map.df = join(nyc_map.points, nyc_map@data, by="id")
# Only plot Manhattan for now
man <- subset(nyc_map.df, BoroCD < 150)
# Make IDs factors & recode to PUMA 
man$BoroCD <- as.factor(man$BoroCD)
man$PUMA <- revalue(man$BoroCD, c('101'='3810', '102'='3810', '103'='3809',
                                  '104'='3807', '105'='3807', '106'='3808',
                                  '107'='3806', '108'='3805', '109'='3802',
                                  '110'='3803', '111'='3804', '112'='3801'))

# Summarize ACS data by PUMA & year
PUMA <- ddply(man_data, .(PUMA, year, language), summarize, count=length(language))

# Exclude Spanish & find next-most-common languages per PUMA
PUMA2 <- group_by(PUMA, PUMA, year)
no_sp <- filter(PUMA2, language != 'Spanish' & year == 2013)
langs <- filter(no_sp, count==max(count))

# Merge most common languages with geo data
data <- merge(man, langs)

# Plot map of 2013 2nd most common languages
ggplot(data, aes(long, lat, group=group, fill=language))+ geom_polygon()+ theme_bw()+ 
  labs(fill="Language", title="Most common languages spoken in Manhattan\n in 2013 (excluding English and Spanish)")+ 
  theme(axis.title=element_blank(), axis.text=element_blank(), axis.ticks=element_blank())

newdata$count.trans <- scale(log(newdata$count), center=TRUE, scale=FALSE)
newdata$year.trans <- scale(newdata$year, center=TRUE, scale=FALSE)
newdata$sum <- droplevels(newdata$language)
contrasts(WashHts$sum) <- contr.sum(10)

#model
for (i in levels(top10$name)) {
      mod <- lm(count.trans ~ year.trans * sum, data = subset(top10, name==i))
      print(i)
      print(summary(mod))
}
