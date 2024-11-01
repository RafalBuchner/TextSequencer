# encoding: utf-8

###########################################################################################################
#
#
#   Palette Plugin
#
#   Read the docs:
#   https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import Glyphs
from GlyphsApp.plugins import PalettePlugin
from textSplitter import splitText


class TextSequencer(PalettePlugin):

    dialog = objc.IBOutlet()
    stringInputMain = objc.IBOutlet()

    stringInputStart = objc.IBOutlet()
    stringInputEnd = objc.IBOutlet()

    stringInputLeft = objc.IBOutlet()
    stringInputRight = objc.IBOutlet()

    def settings(self):
        self.name = "Text Sequencer"
        self.loadNib('IBdialog', __file__)

    @objc.IBAction
    def insert_(self, sender):

        tab = Glyphs.font.currentTab
        if tab is None:
            return

        font = Glyphs.font
        cmap = {
            glyph.unicodeChar(): glyph.name
            for glyph in font.glyphs
            if glyph.unicode is not None
        }
        fontNames = [g.name for g in font.glyphs]
        masterId = None
        try:
            currLayer = font.selectedLayers[0]

            if currLayer is None:
                currMaster = font.masters[tab.masterIndex]
                masterId = currMaster.id
            else:
                masterId = currLayer.associatedMasterId
        except:
            currMaster = font.masters[tab.masterIndex]
            masterId = currMaster.id

        assert masterId is not None, "Master Id is None"

        tabLayers = [layer for layer in tab.layers]
        glyphsToInsert = splitText(self.stringInputMain.stringValue(), cmap)
        glyphsToInsertStart = splitText(self.stringInputStart.stringValue(), cmap)
        glyphsToInsertEnd = splitText(self.stringInputEnd.stringValue(), cmap)
        glyphsToInsertLeft = splitText(self.stringInputLeft.stringValue(), cmap)
        glyphsToInsertRight = splitText(self.stringInputRight.stringValue(), cmap)

        layersToInsert = []

        for name in glyphsToInsert:
            if name in fontNames:
                glyph = font[name]
                layer = glyph.layers[masterId]
                layersToInsert += [layer]

        layersToInsertStart = []

        for name in glyphsToInsertStart:
            if name in fontNames:
                glyph = font[name]
                layer = glyph.layers[masterId]
                layersToInsertStart += [layer]

        layersToInsertEnd = []

        for name in glyphsToInsertEnd:
            if name in fontNames:
                glyph = font[name]
                layer = glyph.layers[masterId]
                layersToInsertEnd += [layer]

        layersToInsertLeft = []

        for name in glyphsToInsertLeft:
            if name in fontNames:
                glyph = font[name]
                layer = glyph.layers[masterId]
                layersToInsertLeft += [layer]

        layersToInsertRight = []

        for name in glyphsToInsertRight:
            if name in fontNames:
                glyph = font[name]
                layer = glyph.layers[masterId]
                layersToInsertRight += [layer]

        if tab.textRange == 0:
            before_selection = []
            selection = tabLayers
            after_selection = []
        else:
            before_selection = tabLayers[: tab.textCursor]
            selection = tabLayers[tab.textCursor: tab.textCursor + tab.textRange]
            after_selection = tabLayers[tab.textCursor + tab.textRange:]

        newTabLayers = before_selection
        newTabLayers += layersToInsertStart
        newTabLayers += layersToInsert
        for layer in selection:
            newTabLayers += (
                layersToInsertLeft + [layer] + layersToInsertRight + layersToInsert
            )
        newTabLayers += layersToInsertEnd
        newTabLayers += after_selection
        print("")
        print("***")
        for layer in newTabLayers:
            if layer.parent.name is None:
                continue
            print("/" + layer.parent.name, end=" ")
        print()
        tab.layers = newTabLayers
        if tab.textRange != 0:
            tab.textRange = (
                len(layersToInsertStart)
                + len(layersToInsertEnd)
                + len(selection) * len(layersToInsert)
                + len(layersToInsert)
                + len(selection)
                + len(layersToInsertLeft)
                + len(selection)
                + len(layersToInsertRight)
                + len(selection)
            )

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__

    # Temporary Fix
    # Sort ID for compatibility with v919:
    _sortID = 0

    @objc.python_method
    def setSortID_(self, id):
        try:
            self._sortID = id
        except Exception as e:
            self.logToConsole("setSortID_: %s" % str(e))

    @objc.python_method
    def sortID(self):
        return self._sortID
