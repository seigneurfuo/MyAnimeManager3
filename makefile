APPNAME=myanimemanager3
APPVERSION=$(shell git show -s --format=%cs | tr - .)

archlinux-build:
	cd "packaging/PKGBUILD"; \
	rm -rf packaging/*.pkg.*; \
	makepkg --syncdeps --force --rmdeps --cleanbuild --clean; \
	rm -rf "MyAnimeManager 3"

archlinux-install:
	cd "packaging/PKGBUILD/dist"; \
	sudo pacman -U $(APPNAME)-$(APPVERSION)-*;

manjaro-build:
	archlinux-build

manjaro-install:
	archlinux-install

dist:
	archlinux-build
