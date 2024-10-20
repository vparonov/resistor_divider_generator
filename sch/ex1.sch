v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -80 -80 -80 -40 {
lab=#net1}
N -80 20 -80 70 {
lab=#net2}
N -130 70 0 70 {
lab=#net2}
N -130 130 -0 130 {
lab=#net3}
C {sky130_fd_pr/res_xhigh_po_1p41.sym} -80 -10 0 0 {name=R12
W=1.41
L=20
model=res_xhigh_po_1p41
spiceprefix=X
 mult=1}
C {sky130_fd_pr/res_xhigh_po_1p41.sym} -130 100 0 0 {name=R1
W=20.0
L=1.41
model=res_xhigh_po_1p41
spiceprefix=X
 mult=1}
C {sky130_fd_pr/res_xhigh_po_1p41.sym} 0 100 0 0 {name=R2
W=20.0
L=1.41
model=res_xhigh_po_1p41
spiceprefix=X
 mult=1}
