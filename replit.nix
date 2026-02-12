{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.sqlite
    pkgs.libuuid
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.zlib
      pkgs.glib
    ];
  };
}
