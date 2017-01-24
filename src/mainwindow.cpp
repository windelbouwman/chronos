#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    m_aboutAct = new QAction("About");

    createMenus();

    m_signal_viewer = new SignalViewer(this);
    setCentralWidget(m_signal_viewer);
}

MainWindow::~MainWindow()
{
    delete m_aboutAct;

    delete ui;
}

void MainWindow::createMenus()
{
    QMenu* fileMenu = menuBar()->addMenu(tr("Help"));
    fileMenu->addAction(m_aboutAct);
}
