pyuic4-2.7 mainUi.ui -o mainUi.py
pyuic4-2.7 statusBarUi.ui -o statusBarUi.py
pyuic4-2.7 serialIndicatorUi.ui -o serialIndicatorUi.py

pyuic4-2.7 side_barUi.ui -o side_barUi.py
pyuic4-2.7 tab_serialUi.ui -o tab_serialUi.py
rem pyuic4-2.7 tab_sourceUi.ui -o tab_sourceUi.py
#pyuic4-2.7 tab_calibrationUi.ui -o tab_calibrationUi.py
pyuic4-2.7 tab_objectsUi.ui -o tab_objectsUi.py
pyuic4-2.7 tab_regionsUi.ui -o tab_regionsUi.py
pyuic4-2.7 tab_blindspotUi.ui -o tab_blindspotUi.py
pyuic4-2.7 tab_markersUi.ui -o tab_markersUi.py
#pyuic4-2.7 CalibPopUp.ui -o CalibPopUp.py
pyuic4-2.7 main_tab_pageUi.ui -o main_tab_pageUi.py

pyrcc4-2.7 icons.qrc -o icons_rc.py
pyrcc4-2.7 images.qrc -o images_rc.py