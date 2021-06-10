with import <nixpkgs> {};
let
  unstable = import <nixos-unstable> {};
in mkShell {
  buildInputs = [
    unstable.python38Packages.pytorchWithCuda
    unstable.python38Packages.torchvision
    (python38.withPackages (ps: with ps; let
        in [
    ]))
  ];
  PYTHONPATH="";
  LIBRAW_LIB="${pkgs.libraw.lib}/lib";
  LIBRAW_BIN="${pkgs.libraw}/bin";
  LIBRAW_INCLUDE="${pkgs.libraw.dev}/include";
}
