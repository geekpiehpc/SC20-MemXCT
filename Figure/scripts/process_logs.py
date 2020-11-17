import re
import os
import json

spat_size = re.compile(r'SPATIAL TILE SIZE\s+:\s+(\d+)')

def process_log(filename):
    with open(filename) as f:
        lines = f.readlines()
    
    params = {}
    eval_times = {}
    eval_result = {}
    
    for line in lines:
        if line.startswith('SPATIAL TILE SIZE'):
            params['SPATSIZE'] = int(line.split(':')[1].strip())
        elif line.startswith('SPECTRAL TILE SIZE'):
            params['SPECSIZE'] = int(line.split(':')[1].strip())
        elif line.startswith('NUMBER OF PROCESSES'):
            params['NP'] = int(line.split(':')[1].strip())
        elif line.startswith('NUMBER OF THRD./PROC.'):
            params['NT'] = int(line.split(':')[1].strip())
        elif line.startswith('SPATIAL INDEXING'):
            params['SPATINDEX'] = int(line.split(':')[1].strip())
        elif line.startswith('PROJECTION BLOCK SIZE'):
            params['PROJBLOCK'] = int(line.split(':')[1].strip())
        elif line.startswith('BACKPROJECTION BLOCK SIZE'):
            params['BACKBLOCK'] = int(line.split(':')[1].strip())
        elif line.startswith('PROJECTION BUFFER SIZE'):
            params['PROJBUFF'] = int(line.split(':')[1].strip().split()[0])
        elif line.startswith('BACKPROJECTION BUFFER SIZE'):
            params['BACKBUFF'] = int(line.split(':')[1].strip().split()[0])
        elif line.startswith('SINOGRAM FILE'):
            params['DATASET'] = line.split('/')[-1].split('_')[0]
        elif line.startswith('recon: '):
            match = re.match(r'recon: (\S+) proj: (\S+) \((\S+) (\S+) (\S+)\) backproj: (\S+) \((\S+) (\S+) (\S+)\) ctime: (\S+) wtime: (\S+)', line)
            times = [float(x) for x in match.groups()]
            labels = ['recon', 'proj', 'proj_calc', 'proj_alltoall', 'proj_reduce', 'back', 'back_reduce', 'back_alltoall', 'back_calc', 'basic_kernel', 'allreduce']
            eval_times.update(dict(zip(labels, times)))

        elif line.startswith('RAY-TRACING TIME:'):
            eval_times['raytrace'] = float(line.split(':')[1].strip())
        elif line.startswith('TRANSPOSITION TIME:'):
            eval_times['transport'] = float(line.split(':')[1].strip())

        elif line.startswith('CSR STORAGE:'):
            if 'STORAGE EFFICIENCY' in line:
                match = re.match(r'CSR STORAGE: \S+ \(\S+ GB\) buffnzmax: \S+ STORAGE EFFICIENCY: (\S+) DATA REUSE: (\S+)', line)
                if 'proj_matrix_block' not in eval_result:
                    eval_result['proj_matrix_block_effi'] = float(match.group(1))
                    eval_result['proj_matrix_block_reuse'] = float(match.group(2))
                else:
                    eval_result['back_matrix_block_effi'] = float(match.group(1))
                    eval_result['back_matrix_block_reuse'] = float(match.group(2))

        elif line.startswith('BLOCKING TIME:'):
            if 'proj_matrix_block' not in eval_times:
                eval_times['proj_matrix_block'] = float(line.split(':')[1].strip())
            else:
                eval_times['back_matrix_block'] = float(line.split(':')[1].strip())

        elif line.startswith('TIME:'):
            if 'proj_matrix_fill' not in eval_times:
                eval_times['proj_matrix_fill'] = float(line.split(':')[1].strip())
            else:
                eval_times['back_matrix_fill'] = float(line.split(':')[1].strip())

        elif line.startswith('PREPROCESSING TIME:'):
            eval_times['preprocess'] = float(line.split(':')[1].strip())

        elif line.startswith('proj:'):
            if 'GFLOPS' in line:
                match = re.match(r'proj: (\S+) s \((\S+) GFLOPS\) backproj: (\S+) s \((\S+) GFLOPS\) avGFLOPS: (\S+) totGFLOPS: (\S+)', line)
                times = [float(x) for x in match.groups()]
                labels = ['proj_time', 'proj_flops', 'back_time', 'back_flops', 'aver_flops', 'total_flops']
                eval_result.update(dict(zip(labels, times)))
            else:
                match = re.match(r'proj: (\S+) GB/s back: (\S+) GB/s av: (\S+) GB/s tot: (\S+) GB/s', line)
                times = [float(x) for x in match.groups()]
                labels = ['proj_band', 'back_band', 'aver_band', 'total_band']
                eval_result.update(dict(zip(labels, times)))

        elif line.startswith('Total Time:'):
            eval_result['total_time'] = float(line.split(':')[1].strip())

    # print(params)
    # print(eval_times)
    # print(eval_result)
    return params, eval_times, eval_result


def process_logs(folder):
    files = os.listdir(folder)
    data = []
    i = 0
    for file in files:
        i += 1
        if i % 100 == 0:
            print(f'Processing {i}th file...')
        if 'log' in file:
            filename = os.path.join(folder, file)
            params, eval_times, eval_result = process_log(filename)
            if 'total_time' not in eval_result:
                continue
            data.append({
                'params': params,
                'times': eval_times,
                'result': eval_result,
            })
    return data
    

if __name__ == "__main__":
    import sys
    folder_name = sys.argv[1]
    output_name = sys.argv[2]
    
    data = process_logs(folder_name)
    
    with open(output_name, 'w+') as f:
        json.dump(data, f, indent=4)
