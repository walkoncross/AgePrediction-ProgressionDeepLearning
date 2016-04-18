graph = Graph() 
graph.add_input(name='input1', input_shape=(1,120,120)) 
graph.add_input(name='input2', input_shape=(1,120,120))
graph.add_node(Convolution2D(64, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv1_1',input='input1')
graph.add_node(Convolution2D(64, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv1_2',input='conv1_1')
graph.add_node(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),name='max_conv1_1',input='conv1_2')
graph.add_node(BatchNormalization(),name='batchnorm_conv1_1',input='max_conv1_1')
graph.add_node(Convolution2D(128, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv1_3',input='batchnorm_conv1_1')
graph.add_node(Convolution2D(128, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv1_4',input='conv1_3')
graph.add_node(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),name='max_conv1_2',input='conv1_4')
graph.add_node(BatchNormalization(),name='batchnorm_conv1_2',input='max_conv1_2')
graph.add_node(Convolution2D(256, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv1_5',input='batchnorm_conv1_2')
graph.add_node(Convolution2D(256, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv1_6',input='conv1_5')
graph.add_node(Convolution2D(64, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv2_1',input='input2')
graph.add_node(Convolution2D(64, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv2_2',input='conv2_1')
graph.add_node(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),name='max_conv2_1',input='conv2_2')
graph.add_node(BatchNormalization(),name='batchnorm_conv2_1',input='max_conv2_1')
graph.add_node(Convolution2D(128, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv2_3',input='batchnorm_conv2_1')
graph.add_node(Convolution2D(128, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv2_4',input='conv2_3')
graph.add_node(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),name='max_conv2_2',input='conv2_4')
graph.add_node(BatchNormalization(),name='batchnorm_conv2_2',input='max_conv2_2')
graph.add_node(Convolution2D(256, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv2_5',input='batchnorm_conv2_2')
graph.add_node(Convolution2D(256, 3, 3, border_mode='valid',init='he_normal',activation='relu'),name='conv2_6',input='conv2_5')

graph.add_shared_node(Convolution2D(256,3,3,activation='relu',init='he_normal',border_mode="valid"),name='combined_layer_1',inputs=['conv1_6','conv2_6'],merge_mode='sum')
graph.add_node(Flatten(), name='flatten_layer',input='combined_layer_1')
graph.add_node(Dense(256,activation='relu'),name='combined_dense_layer_1',input='flatten_layer')
graph.add_node(Dense(2,activation='softmax'),name='output_layer',input='combined_dense_layer_1')
graph.add_output(name='output1',input='output_layer')
graph.compile('sgd',{'output1':'binary_crossentropy'})
graph.get_config(verbose=1)
graph.fit({'input1':XTrain1,'input2':XTrain2,'output1':y_train2},batch_size=32,nb_epoch=5)