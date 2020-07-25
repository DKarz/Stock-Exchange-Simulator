

buybutton = """QPushButton { text-align: left;
            background: lime;};
            """


sellbutton = """QPushButton { text-align: left;
            background: red;};
            """


# buybutton = """QPushButton { text-align: left;
#             background: qlineargradient(spread:pad, x1:0.0568182, y1:0.126, x2:0.75, y2:0.227, stop:0.0738636 rgba(0, 255, 0, 255), stop:0.840909 rgba(0, 136, 0, 255));};
#             """
#
#
# sellbutton = """QPushButton { text-align: left;
#             background: qlineargradient(spread:pad, x1:0.0568182, y1:0.126, x2:0.75, y2:0.227, stop:0.0738636 rgba(255, 0, 0, 255), stop:0.840909 rgba(167, 0, 0, 255));};
#             """

barstyle = """QPushButton {
    text-align: right;
    color: rgba(51, 0, 51, 255);
    border-style: outset;
    border-width: 2px;
    border-color: beige;
    font: bold 14px;
    min-width: 10em;
    padding: 6px;
    background: qlineargradient(spread:pad, x1:0.0568182, y1:0.126, x2:0.75, y2:0.227, stop:0.0738636 rgba(192, 192, 192, 255), stop:0.840909 rgba(210, 210, 210, 255));
}"""


barstyle1 = """QPushButton {
    text-align: right;
    font: bold 14px;
    color: rgba(51, 0, 51, 255);
}"""

barstyle2 = """QPushButton {
    text-align: right;
    font: bold 14px;
    color: rgba(255, 255, 255, 255);
}"""

gradient1 = """ QPushButton {background: qlineargradient(spread:pad, x1:0.0568182, y1:0.126, x2:0.75, y2:0.227, stop:0.0738636 rgba(192, 192, 192, 255), stop:0.840909 rgba(210, 210, 210, 255));}"""

gr2 = """QPushButton { background: qlineargradient(spread:pad, x1:0.0568182, y1:0.126, x2:0.75, y2:0.227, stop:0.0738636 rgba(0, 255, 0, 255), stop:0.840909 rgba(0, 136, 0, 255));};
            """
gr3 = """QPushButton { background: qlineargradient(spread:pad, x1:0.0568182, y1:0.126, x2:0.75, y2:0.227, stop:0.0738636 rgba(255, 0, 0, 255), stop:0.840909 rgba(167, 0, 0, 255));};
            """


# news = """QPushButton {
#
#     color: rgba(51, 0, 51, 255);
#     border-style: outset;
#     border-width: 2px;
#     border-color: beige;
#     font: bold 14px;
#     min-width: 10em;
#     padding: 6px;
#     background: qlineargradient(spread:pad, x1:0.0568182, y1:0.126, x2:0.75, y2:0.227, stop:0.0738636 rgba(192, 192, 192, 255), stop:0.840909 rgba(210, 210, 210, 255));
# }"""

news = """QPushButton {
    color: rgba(51, 0, 51, 255);
    background: rgba(192, 192, 192, 255);
}"""

res = """QLabel  { text-align: center;
           };
            """
buybuttonFus = """QPushButton { text-align: left;
            background: lime;};
            """
sellbuttonFus = """QPushButton { text-align: left;
            background: red;};
            """

buttonY = """QPushButton { text-align: left;
            background: rgb(255,223,0);};
            """
slider = """QSlider::groove:horizontal {
    border: 1px solid #999999;
    height: 8px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
    margin: 2px 0;
}

QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
    border: 1px solid #5c5c5c;
    width: 18px;
    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
    border-radius: 3px;
}"""
