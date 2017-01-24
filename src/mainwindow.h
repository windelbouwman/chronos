#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "signalviewer.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

    void createMenus();

private:
    Ui::MainWindow *ui;

    QAction* m_aboutAct;
    SignalViewer* m_signal_viewer;
};

#endif // MAINWINDOW_H
