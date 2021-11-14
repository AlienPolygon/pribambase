# Pribambase

Pribambase is a small tool that connects Aseprite and Blender, to allow painting with instant viewport feedback and all functionality of external editor at the same time. It also adds a few shortcuts like displaying the UV map in Aseprite or setting up a grid-scaled pixelart reference in the viewport.

Currently, the addon has mostly one-way workflow where you paint in Ase and not much in Blender. Better bidirectional workflow ~~is quite a task tell ya what~~ is planned in future versions.

* [Download](https://lampysprites.itch.io/pribambase) packaged version for your platform
* [Geeting Started](https://github.com/lampysprites/pribambase/wiki/Getting-Started) after installing, look there
* [Reference](https://github.com/lampysprites/pribambase/wiki/Reference) explains each button and setting
* [Itchio forum](https://lampysprites.itch.io/pribambase/community) to show off your work or ask for help
* [Issue tracker](https://github.com/lampysprites/pribambase/issues) for bug reports and feature requests. Kindly don't submit non-technical help requests.

​Although the entire project is distributed free of charge, I highly encourage you to support it financially sooner or later, as if it was on blen\*\*\*arket or flip\*\*\*rmals. There's still work left to do, and it'd be pretty great to be able to do it sooner.

## Setup

_[Video version](https://youtu.be/70wyQhKyxFw) - all thanks to [frozenMeatpopsicle](https://twitter.com/fznmeatpopsicle)_

This plugin consists of **two** parts: for Aseprite and for Blender. Get pre-packaged version for your OS [on Itchio](https://lampysprites.itch.io/pribambase). **Do not** download repo ZIP, it won't just work without extra steps.

### Prerequisites

* [Blender](https://Blender.org) recommended version 2.83 or later, preferrably latest. Minimum version is 2.80, but performance and stability are significantly worse
* [Aseprite](https://Aseprite.org) minimum version 1.2.30 or 1.3-beta7. Trial version won't work

### Installing Aseprite plugin
1. Launch Aseprite and drag the file called __pribambase-aseprite__ into the window
1. Press Install
1. Restart Aseprite

After that, a new menu option called **Sync** should appear in the **File** menu

### Installing Blender plugin
1. In __Edit > Preferences > Addons__ click __Install__ and chose the file called __pribambase-blender-\[YOUR OS\]__
1. After the addon appears in the list, check the box next to its name to activate it. The app might freeze for several seconds
1. Save preferences from the "burger" menu

After that, a new section called **Sync** will appear in **N > Tools** tab in viewport, and a new menu called **Sprite** will appear in the Image/uv editor.

## Usage

After the plugins are installed, turn each of them on before drawing: nn blender press __Connect__ on top of the plugin's panel in the viewport, in Aseprite press __File > Sync__ . After that you can:

* Open any texture used in blendfile normally in Aseprite, and it will be updated in Blender as you paint. This applies to both textures created normally with blender, and textures set up by the plugin
* Use **Image Editor > Sprite** menu to load aseprite files as textures, or create new ones
* Use **Sprite > Send UV** to show the UV Map in aseprite

See [Reference](Reference) for all features.

## Source

Source for [aseprite plugin](https://github.com/aseprite/api/blob/main/api/plugin.md) is the `client/` folder. The repo root is the [blender plugin](https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html#install-the-add-on). For using source, you'd probably want to symlink them to extension/addon locations.

Third party dependencies aren't stored in the repo. Download them from PyPI to `thirdparty` folder, or fetch with PIP:

```shell
cd to/project/root

## for your platform
pip download -d thirdparty -r requirements.txt

## for different platforms; the platform tags tags go look up on PyPI
pip download -d thirdparty --platform win32 --only-binary=:all: -r requirements.txt
```

## License
In accordance with Blender developers' [wishes](https://www.blender.org/about/license/), the addon is distributed under GPL-3.0 license.
See COPYING for full license text.
Specific files or libraries might be also available under different terms, see included comment or package licenses.

## Acknowledgements
Async loop handling is based on [Blender Cloud Addon](https://cloud.blender.org/services)
