import numpy as np
import os
from tensorflow import keras
from sklearn.feature_extraction.text import CountVectorizer
from utils import parameter_parser
from utils import write_output


def Extraction(retdec_path , file_input_path):
    cmd = retdec_path + '-output ' + file_input_path.split('/')[-1]
    os.system(cmd)
    f = open('./' + file_input_path.split('/')[-1] + '.dsm', 'r')
    op = []
    for i in f.readlines():
        if('\t' in i):
            i = i.split('\t')[1].split(' ')[0]
            op.append(i)
    return op

def function(times_list_1 , times_list_2):
    a = 1
    e = 2.71
    result = 0
    for l in times_list_1:
        min_list = []
        for j in times_list_2:
            min_list.append(abs(l - j - 1))
        number = min(min_list)
        tmp = 2/(1+(a*(e**(number))))
        result += tmp
    return result

def get_sorted_index(count):
    result = []
    for i in range(100):
        m = count.index(max(count))
        result.append(m)
        count[m] = -1
    return result

def producer(times_count , seq):
    tmp = []
    sorted_index = get_sorted_index(times_count)
    for i in sorted_index:
        tmp.append((i , get_index(seq , i)))
    return tmp

def make_graph(opcode_seq):
    top_feature = (np.load('./top_100_feature.npy')).tolist()
    sample = ''
    for i in top_feature:
        sample += (i + ' ')
    table = dict(zip(feature_name,range(100)))
    opcode_clear = []
    opcode_times = ''
    for i in opcode_seq:
        if i in top_feature:
            opcode_clear.append(i)
            opcode_times += (i +' ')
    vectorizer = CountVectorizer()
    corpus = []
    corpus = [sample,opcode_times]
    opcode_times = vectorizer.fit_transform(corpus).toarray()[1,:]
    for i in range(len(opcode_clear)):
        opcode_clear[j] = table[opcode_clear[j]]
    opcode_clear = np.array(opcode_clear)
    result = producer(opcode_times.tolist(),opcode_clear)
    matrix = np.zeros((100,100))
    flag = 0
    for i in range(100):
        if(result[i][1] == []):
            break
        for k in range(5):
            try:
                if(result[i+k][1] == []):
                    flag = 1
                    break
                matrix[result[i][0] , result[i+k][0]] = function(result[i][1],result[i+k][1])
            except:
                pass
        if(flag == 1):
            break
    return matrix

def get_first_two_eigenvector(matrix):
    val,vec = np.linalg.eig(matrix)
    val = val.tolist()
    vec = vec.tolist()
    max_number_index = []
    for i in range(2):
        j = val.index(max(val))
        max_number_index.append(j)
        val[j] = -1
    two_eigenvector = vec[max_number_index[0]]+vec[max_number_index[1]]
    return two_eigenvector

def main():
    result = [-1]
    if args.classify:
        labels = ['BenignWare','Android','Mirai','Bashlite','Hajime','Dofloo','Pnscan','Tsunami','Unknown','Xorddos']
    labels = ['Malware','Benignware']
    try:
        opcode_sequence = Extraction(args.retdec_path ,args.input_path)
    except:
        print('fail to extract the Opcode.')
        print(result)
        write_output(args.input_path, args.output_path, result, labels)
        return result
   
    try:
        feature = make_graph(opcode_sequence)
    except:
        print('fail to extract the feature.')
        print(result)
        write_output(args.input_path, args.output_path, result, labels)
        return result

    feature = get_first_two_eigenvector(feature)
    feature = np.reshape(feature,(1,200))
    if args.classify:
        model = keras.models.load_model('./FC.pb')
        result = model.predict(feature)[0]
        print(result)
        write_output(args.input_path, args.output_path, result, labels)
        return result
    model = keras.models.load_model('./MD.pb')
    result = model.predict(feature)[0]
    print(result)
    write_output(args.input_path, args.output_path, result, labels)
    return result

if __name__=='__main__':
    args = parameter_parser()
    main(args)    