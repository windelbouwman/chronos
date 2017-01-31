#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "signalviewer.h"
#include "timespanselectionwidget.h"
#include "sourcesselector.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    void createMenus();
    void createDockWindows();

    Ui::MainWindow *ui;

    QMenu* m_viewMenu;
    QAction* m_aboutAct;
    SignalViewer* m_signal_viewer;
    SourcesSelector* m_data_sources_view;

    TimespanSelectionWidget* m_timespan_selector;
};

#endif // MAINWINDOW_H
