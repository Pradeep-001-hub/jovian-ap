#include "fvCFD.H"

using namespace Foam;

int main(int argc, char *argv[])
{
    argList::addNote
    (
        "JOVIAN-AP rotating shallow-water solver"
    );

    #include "setRootCase.H"
    #include "createTime.H"
    #include "createMesh.H"

    Info<< "\nJOVIAN-AP solver starting" << endl;

    Info<< "OpenFOAM time: "
        << runTime.timeName() << endl;

    Info<< "Mesh cells: "
        << mesh.nCells() << endl;

    Info<< "\nSolver framework initialisation complete."
        << endl;

    Info<< "The shallow-water equations have not yet been implemented."
        << endl;

    return 0;
}