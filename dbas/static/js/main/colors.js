function Colors() {
    'use strict';
    // https://www.google.com/design/spec/style/color.html#color-color-palette

    this.all = [
        this.get_red(), this.get_pink(), this.get_purple(), this.get_deepPurple(), this.get_indigo(),
        this.get_blue(), this.get_lightBlue(), this.get_cyan(), this.get_teal(), this.get_green(),
        this.get_lightGreen(), this.get_lime(), this.get_yellow(), this.get_amber(), this.get_orange(),
        this.get_deepOrange(), this.get_brown(), this.get_grey(), this.get_blueGrey()];
}

/**
 * Returns a value in the range of 50, 100, 200, ... 900 if index is out of 0-9
 *
 * @param index integer between 0 and 9
 * @returns {*}
 */
Colors.prototype.index_matcher = function(index){
    'use strict';
    var scales = {
        0: 50,
        1: 100,
        2: 200,
        3: 300,
        4: 400,
        5: 500,
        6: 600,
        7: 700,
        8: 800,
        9: 900,
    };
    return scales[index];
};

Colors.prototype.get_red = function () {
    'use strict';
    return {
        50: '#ffebee',
        100: '#ffcdd2',
        200: '#ef9a9a',
        300: '#e57373',
        400: '#ef5350',
        500: '#f44336',
        600: '#e53935',
        700: '#d32f2f',
        800: '#c62828',
        900: '#b71c1c'
    };
};
Colors.prototype.get_pink = function () {
    'use strict';
    return {
        50: '#fce4ec',
        100: '#f8bbd0',
        200: '#f48fb1',
        300: '#f06292',
        400: '#ec407a',
        500: '#e91e63',
        600: '#d81b60',
        700: '#c2185b',
        800: '#ad1457',
        900: '#880e4f'
    };
};
Colors.prototype.get_purple = function () {
    'use strict';
    return {
        50: '#f3e5f5',
        100: '#e1bee7',
        200: '#ce93d8',
        300: '#ba68c8',
        400: '#ab47bc',
        500: '#9c27b0',
        600: '#8e24aa',
        700: '#7b1fa2',
        800: '#6a1b9a',
        900: '#4a148c'
    };
};
Colors.prototype.get_deepPurple = function () {
    'use strict';
    return {
        50: '#ede7f6',
        100: '#d1c4e9',
        200: '#b39ddb',
        300: '#9575cd',
        400: '#7e57c2',
        500: '#673ab7',
        600: '#5e35b1',
        700: '#512da8',
        800: '#4527a0',
        900: '#311b92'
    };
};
Colors.prototype.get_indigo = function () {
    'use strict';
    return {
        50: '#e8eaf6',
        100: '#c5cae9',
        200: '#9fa8da',
        300: '#7986cb',
        400: '#5c6bc0',
        500: '#3f51b5',
        600: '#3949ab',
        700: '#303f9f',
        800: '#283593',
        900: '#1a237e'
    };
};
Colors.prototype.get_blue = function () {
    'use strict';
    return {
        50: '#e3f2fd',
        100: '#bbdefb',
        200: '#90caf9',
        300: '#64b5f6',
        400: '#42a5f5',
        500: '#2196f3',
        600: '#1e88e5',
        700: '#1976d2',
        800: '#1565c0',
        900: '#0d47a1'
    };
};
Colors.prototype.get_lightBlue = function () {
    'use strict';
    return {
        50: '#e1f5fe',
        100: '#b3e5fc',
        200: '#81d4fa',
        300: '#4fc3f7',
        400: '#29b6f6',
        500: '#03a9f4',
        600: '#039be5',
        700: '#0288d1',
        800: '#0277bd',
        900: '#01579b'
    };
};
Colors.prototype.get_cyan = function () {
    'use strict';
    return {
        50: '#e0f7fa',
        100: '#b2ebf2',
        200: '#80deea',
        300: '#4dd0e1',
        400: '#26c6da',
        500: '#00bcd4',
        600: '#00acc1',
        700: '#0097a7',
        800: '#00838f',
        900: '#006064'
    };
};
Colors.prototype.get_teal = function () {
    'use strict';
    return {
        50: '#e0f2f1',
        100: '#b2dfdb',
        200: '#80cbc4',
        300: '#4db6ac',
        400: '#26a69a',
        500: '#009688',
        600: '#00897b',
        700: '#00796b',
        800: '#00695c',
        900: '#004d40'
    };
};
Colors.prototype.get_green = function () {
    'use strict';
    return {
        50: '#e8f5e9',
        100: '#c8e6c9',
        200: '#a5d6a7',
        300: '#81c784',
        400: '#66bb6a',
        500: '#4caf50',
        600: '#43a047',
        700: '#388e3c',
        800: '#2e7d32',
        900: '#1b5e20'
    };
};
Colors.prototype.get_lightGreen = function () {
    'use strict';
    return {
        50: '#f1f8e9',
        100: '#dcedc8',
        200: '#c5e1a5',
        300: '#aed581',
        400: '#9ccc65',
        500: '#8bc34a',
        600: '#7cb342',
        700: '#689f38',
        800: '#558b2f',
        900: '#33691e'
    };
};
Colors.prototype.get_lime = function () {
    'use strict';
    return {
        50: '#f9fbe7',
        100: '#f0f4c3',
        200: '#e6ee9c',
        300: '#dce775',
        400: '#d4e157',
        500: '#cddc39',
        600: '#c0ca33',
        700: '#afb42b',
        800: '#9e9d24',
        900: '#827717'
    };
};
Colors.prototype.get_yellow = function () {
    'use strict';
    return {
        50: '#fffde7',
        100: '#fff9c4',
        200: '#fff59d',
        300: '#fff176',
        400: '#ffee58',
        500: '#ffeb3b',
        600: '#fdd835',
        700: '#fbc02d',
        800: '#f9a825',
        900: '#f57f17'
    };
};
Colors.prototype.get_amber = function () {
    'use strict';
    return {
        50: '#fff8e1',
        100: '#ffecb3',
        200: '#ffe082',
        300: '#ffd54f',
        400: '#ffca28',
        500: '#ffc107',
        600: '#ffb300',
        700: '#ffa000',
        800: '#ff8f00',
        900: '#ff6f00'
    };
};
Colors.prototype.get_orange = function () {
    'use strict';
    return {
        50: '#fff3e0',
        100: '#ffe0b2',
        200: '#ffcc80',
        300: '#ffb74d',
        400: '#ffa726',
        500: '#ff9800',
        600: '#fb8c00',
        700: '#f57c00',
        800: '#ef6c00',
        900: '#e65100'
    };
};
Colors.prototype.get_deepOrange = function () {
    'use strict';
    return {
        50: '#fbe9e7',
        100: '#ffccbc',
        200: '#ffab91',
        300: '#ff8a65',
        400: '#ff7043',
        500: '#ff5722',
        600: '#f4511e',
        700: '#e64a19',
        800: '#d84315',
        900: '#bf360c'
    };
};
Colors.prototype.get_brown = function () {
    'use strict';
    return {
        50: '#efebe9',
        100: '#d7ccc8',
        200: '#bcaaa4',
        300: '#a1887f',
        400: '#8d6e63',
        500: '#795548',
        600: '#6d4c41',
        700: '#5d4037',
        800: '#4e342e',
        900: '#3e2723'
    };
};
Colors.prototype.get_grey = function () {
    'use strict';
    return {
        50: '#fafafa',
        100: '#f5f5f5',
        200: '#eeeeee',
        300: '#e0e0e0',
        400: '#bdbdbd',
        500: '#9e9e9e',
        600: '#757575',
        700: '#616161',
        800: '#424242',
        900: '#212121'
    };
};
Colors.prototype.get_blueGrey = function () {
    'use strict';
    return {
        50: '#eceff1',
        100: '#cfd8dc',
        200: '#b0bec5',
        300: '#90a4ae',
        400: '#78909c',
        500: '#607d8b',
        600: '#546e7a',
        700: '#455a64',
        800: '#37474f',
        900: '#263238'
    };
};

/**
 *
 * @param shade is 50, 100, 200, 300, 400, 500, 600, 700, 800 or 900
 * @returns {Array}
 */
Colors.prototype.getAllAsHEX = function (shade) {
    'use strict';
    var color_array = [];
    $.each(this.all, function (index, color) {
        color_array.push(color[shade]);
    });
    return color_array;
};

/**
 *
 * @param shade is 50, 100, 200, 300, 400, 500, 600, 700, 800 or 900
 * @param alpha is in [0.0, 1.0]
 * @returns {Array}
 */
Colors.prototype.getAllAsRGB = function (shade, alpha) {
    'use strict';
    var tmp_array = this.getAllAsHEX(shade);
    var color_array = [];
    var _this = this;
    $.each(tmp_array, function (index, color) {
        color_array.push(_this.hexToRGB(color, alpha));
    });
    return color_array;
};

Colors.prototype.hexToRGB = function (hex, alpha) {
    'use strict';
    var r = parseInt(hex.slice(1, 3), 16);
    var g = parseInt(hex.slice(3, 5), 16);
    var b = parseInt(hex.slice(5, 7), 16);
    var rgba = 'rgba(' + r + ', ' + g + ', ' + b;
    if (alpha) {
        return rgba + ', ' + alpha + ')';
    } else {
        return rgba + ')';
    }
};
