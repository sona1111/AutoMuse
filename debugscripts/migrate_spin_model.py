import torch

init_sketch2pose = "C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/models/spin_model_smplx_eft_18.pt"
init_spin = "C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/models/spin_model_original.pt"
out_spin = "C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/models/spin_model_updated.pt"

init_sketch2pose_m = torch.load(init_sketch2pose)
init_spin_m = torch.load(init_spin)

for key in ('init_pose', 'init_shape', 'init_cam'):
    init_spin_m['model'][key] = init_sketch2pose_m['model'][key]

torch.save(init_spin_m, out_spin)
