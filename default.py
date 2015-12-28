# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# The Heritage Channnel - video addon for Kodi Helix / Isengard. Videos from cultural, natural, scientific, academic, technical and other heritage organisations from across the world.
# This addon was modified from the BBQ Pit Boys plugin (http://addons.tvaddons.ag/show/plugin.video.barbecueweb/)
# These addons depends upon the Youtube addon by Bromix (http://kodi.wiki/view/Add-on:YouTube), so install that as well
#
# Version 1.0.1 with 35 channels / 9-8-2015 by ookgezellig@gmail.com
# See also http://addons.kodi.tv/show/plugin.video.heritagechannel
# ------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# ------------------------------------------------------------

# TODO in next release: Derive icons from Twitter, this is a good source for square icons. Needs resizing to 256x256 and converting from .jpg to .png . Checkout Python Image Library

import os
import sys
import plugintools
from addon.common.addon import Addon


addonID = 'plugin.video.heritagechannel'
addon = Addon(addonID, sys.argv)
local = plugintools.xbmcaddon.Addon(id=addonID)
path = local.getAddonInfo('path')

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

institutionspath = os.path.join(path, 'resources', 'data', "institutions.csv")  # local csv = data/institutions.csv
mainfanart = os.path.join(path,'fanart.jpg')
citiesicon = os.path.join(path, 'resources', 'media', "cities.png")
countriesicon = os.path.join(path, 'resources', 'media', "countries.png")

#debugfile3 = open(os.path.join(path, 'resources', 'data', "debugfile3.txt"), 'w')
#debugfile3.write("splitlist="+str(sl)+"\n\n")
#debugfile3.close()

# Name of institution, City, Countrycode, Youtube channel ID, abbreviation of institute (for icons and fanart)
# Put in in list chi[]
chi = []
chi = plugintools.read_local_csv(institutionspath)
# Break down chi[]. Set OrganisationName, city, countrycode,YoutubeChannel-ID, abbreviation, local thumb and local fanart for every CH institution
chi_name, chi_city, chi_countrycode, chi_countryname, chi_YOUTUBE_CHANNEL, chi_abbrev, chi_twitterHandle, chi_thumb, chi_fanart = (
    [] for i in range(9))

# Strip leading and traling blanks from list entries, as well as multiple inner spaces
# See http://bytes.com/topic/python/answers/590441-how-strip-mulitiple-white-spaces
for i in range(len(chi)):
    chi_name.append(" ".join(chi[i][0].split()))
    chi_city.append(" ".join(chi[i][1].split()))
    chi_countrycode.append(chi[i][2].strip())
    chi_countryname.append(
        plugintools.lookup_countryname(chi_countrycode[i].strip()))
    chi_YOUTUBE_CHANNEL.append(chi[i][3].strip())
    chi_abbrev.append(chi[i][4].strip())
    chi_thumb.append(
        os.path.join(path, 'resources', 'media', 'icons', "icon_" + chi_abbrev[i] + ".png"))
    chi_fanart.append(os.path.join(path, 'resources', 'media', 'fanarts',
                                   "fanart_" + chi_abbrev[i] + ".jpg"))

def BrowseByCountry():
    #fill list alphabetically with unique countrycodes
    unique_countrycode=[]
    for countrycode in chi_countrycode:
        if countrycode not in unique_countrycode:
            unique_countrycode.append(countrycode)
            sorted_unique_countrycode=sorted(unique_countrycode)
    #make menu alphabetically
    for code in sorted_unique_countrycode:
        countryflag = os.path.join(path, 'resources', 'media', 'countryflags', code + ".png")
        li = plugintools.xbmcgui.ListItem(plugintools.lookup_countryname(code.strip()), iconImage=str(countryflag), thumbnailImage="")
        li.setProperty('fanart_image', mainfanart)
        plugintools.xbmcplugin.addDirectoryItem(handle=addon_handle, url=base_url+"?countrycode="+str(code.strip()) , listitem=li,isFolder=True)
    plugintools.close_item_list()

def ShowOrganisationsFromCountry(countrycode):
    for chirow in chi:
        if chirow[2].strip() == countrycode:
            plugintools.add_item(
            # See http://bytes.com/topic/python/answers/590441-how-strip-mulitiple-white-spaces
            title=" ".join(chirow[0].split()) + ", " + " ".join(chirow[1].split()) + ", " + plugintools.lookup_countryname(chirow[2].strip()),
            url="plugin://plugin.video.youtube/user/" + chirow[3].strip() + "/",
            thumbnail=os.path.join(path, 'resources', 'media', 'icons', "icon_" + chirow[4].strip() + ".png"),
            fanart=os.path.join(path, 'resources', 'media', 'fanarts', "fanart_" + chirow[4].strip() + ".jpg"),
            folder=True)
    plugintools.close_item_list()

def BrowseByCity():
    #fill list alphabetically with unique countrycodes
    unique_city=[]
    for city in chi_city:
        if city not in unique_city:
            unique_city.append(city)
            sorted_unique_city=sorted(unique_city)
    #make menu alphabetically
    for su_city in sorted_unique_city:
        li = plugintools.xbmcgui.ListItem(su_city, iconImage=citiesicon , thumbnailImage="")
        li.setProperty('fanart_image', mainfanart)
        plugintools.xbmcplugin.addDirectoryItem(handle=addon_handle, url=base_url+"?city="+str(su_city), listitem=li,isFolder=True)
    plugintools.close_item_list()

def ShowOrganisationsFromCity(city):
    for chirow in chi:
        # See http://bytes.com/topic/python/answers/590441-how-strip-mulitiple-white-spaces
        if " ".join(chirow[1].split()) == city:
            plugintools.add_item(
            title=" ".join(chirow[0].split()) + ", " + " ".join(chirow[1].split()) + ", " + plugintools.lookup_countryname(chirow[2].strip()),
            url="plugin://plugin.video.youtube/user/" + chirow[3].strip() + "/",
            thumbnail=os.path.join(path, 'resources', 'media', 'icons', "icon_" + chirow[4].strip() + ".png"),
            fanart=os.path.join(path, 'resources', 'media', 'fanarts', "fanart_" + chirow[4].strip() + ".jpg"),
            folder=True)
    plugintools.close_item_list()

def main_list(params):
    plugintools.log("heritagechannel.main_list " + repr(params))
    for j in range(len(chi)):
        plugintools.add_item(
            title=chi_name[j] + ", " + chi_city[j] + ", " + chi_countryname[j],
            url="plugin://plugin.video.youtube/user/" + chi_YOUTUBE_CHANNEL[j] + "/",
            thumbnail=chi_thumb[j],
            fanart=chi_fanart[j],
            folder=True)

def run():
    # Main menu
    if sys.argv[2] == "":
        plugintools.log("heritagechannel.run")
        li1 = plugintools.xbmcgui.ListItem("[I]Filter by country[/I]", iconImage=countriesicon, thumbnailImage="")
        li1.setProperty('fanart_image', mainfanart)
        plugintools.xbmcplugin.addDirectoryItem(handle=addon_handle, url=base_url+"?browsebycountry", listitem=li1,isFolder=True)
        li2 = plugintools.xbmcgui.ListItem("[I]Filter by city[/I]", iconImage=citiesicon, thumbnailImage="")
        li2.setProperty('fanart_image', mainfanart)
        plugintools.xbmcplugin.addDirectoryItem(handle=addon_handle, url=base_url+"?browsebycity", listitem=li2,isFolder=True)
        # Get params
        params = plugintools.get_params()
        main_list(params)
        plugintools.close_item_list()
    # Browse By Country menu
    elif sys.argv[2] == "?browsebycountry":
        BrowseByCountry()
    # Browse By City menu
    elif sys.argv[2] == "?browsebycity":
        BrowseByCity()
    # Show menu: institutions in selected country
    elif "countrycode" in sys.argv[2]:
        sl=plugintools.splitOnQuestionmarkAndEquality(sys.argv[2])
        ShowOrganisationsFromCountry(sl[2])
    # Show menu: institutions in selected city
    elif "city" in str(sys.argv[2]):
        sl=plugintools.splitOnQuestionmarkAndEquality(sys.argv[2])
        ShowOrganisationsFromCity(plugintools.urllib.unquote(sl[2]))

run()
