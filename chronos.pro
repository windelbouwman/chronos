#-------------------------------------------------
#
# Project created by QtCreator 2017-01-24T20:03:37
#
#-------------------------------------------------

QT       += core gui charts

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = chronos
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which as been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0


SOURCES += src/main.cpp\
        src/gui/mainwindow.cpp \
    src/gui/signalviewer.cpp \
    src/gui/sourcesselector.cpp \
    src/gui/datasourcemodel.cpp \
    src/gui/timespanselectionwidget.cpp \
    src/data/data_source.cpp \
    src/data/trace_group.cpp \
    src/data/trace_interface.cpp \
    src/data/signal_trace.cpp \
    src/data/tree_item.cpp

HEADERS  += src/gui/mainwindow.h \
    src/gui/signalviewer.h \
    src/gui/sourcesselector.h \
    src/gui/datasourcemodel.h \
    src/gui/timespanselectionwidget.h \
    src/data/data_source.h \
    src/data/trace_group.h \
    src/data/trace_interface.h \
    src/data/signal_trace.h \
    src/data/tree_item.h

FORMS    += src/gui/mainwindow.ui
