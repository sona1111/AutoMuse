import os, shutil


model_dir = os.path.join(os.path.dirname(__file__), "sketch2pose-main\models\models\smplx")

for fname in os.listdir(model_dir):
    if not fname.endswith('.pkl'):
        continue

    tmp_dest = os.path.join(model_dir, 'convert_output.pkl')
    original = os.path.join(model_dir, fname)
    backupfile = os.path.join(model_dir, fname + ".bak")

    print("making backup", backupfile)
    shutil.copyfile(original, backupfile)
    print("converting")

    content = ''
    outsize = 0
    with open(original, 'rb') as infile:
        content = infile.read()
    with open(tmp_dest, 'wb') as output:
        for line in content.splitlines():
            outsize += len(line) + 1
            output.write(line + str.encode('\n'))
            
    print("Done. Saved %s bytes." % (len(content)-outsize))
    os.replace(tmp_dest, original)
    

"""    
original = "word_data.pkl"
destination = "word_data_unix.pkl"

content = ''
outsize = 0
with open(original, 'rb') as infile:
content = infile.read()
with open(destination, 'wb') as output:
for line in content.splitlines():
outsize += len(line) + 1
output.write(line + str.encode('\n'))

print("Done. Saved %s bytes." % (len(content)-outsize))`
"""
