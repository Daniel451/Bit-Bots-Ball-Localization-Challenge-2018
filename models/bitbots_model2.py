import tensorflow as tf


class Model2_FCNN():

    def fcnn_model(self):
        with tf.variable_scope("conv", initializer=self._xavier_normal, dtype=tf.float32):
            #################
            # Encoding part #
            #################
            with tf.variable_scope("conv1"):
                # 150x200x3
                out = tf.layers.conv2d(self.X, 16, [3, 3], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)
                before_maxpool1 = out
                out = tf.layers.max_pooling2d(out, [2, 2], strides=[2, 2], padding="same")
                maxpool1 = out

            with tf.variable_scope("conv2"):
                # 75x100x8
                out = tf.layers.conv2d(out, 32, [3, 3], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)

            with tf.variable_scope("conv3"):
                # 75x100x16
                out = tf.layers.conv2d(out, 32, [3, 3], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)

            with tf.variable_scope("concat1"):
                # 75x100x16
                out = tf.concat([out, maxpool1], 3)
                concat1 = out
                # 75x100x(16+8)

            with tf.variable_scope("conv4"):
                out = tf.layers.max_pooling2d(out, [2, 2], strides=[2, 2], padding="same")
                # 38x50x(16+8)
                maxpool2 = out
                out = tf.layers.conv2d(out, 64, [3, 3], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)

            with tf.variable_scope("conv5"):
                # 38x50x32
                out = tf.layers.conv2d(out, 64, [3, 3], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)

            with tf.variable_scope("concat2"):
                out = tf.concat([out, maxpool2], 3)
                concat2 = out
                # 38x50x(32+24)

            with tf.variable_scope("conv6"):
                # 38x50x(32+24)
                out = tf.layers.conv2d(out, 128, [3, 3], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)
                # 38x50x64

            with tf.variable_scope("conv7"):
                # 38x50x64
                out = tf.layers.conv2d(out, 128, [3, 3], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)
                # 38x50x64


            #################
            # Decoding part #
            #################
            with tf.variable_scope("concat4"):
                # 38x50x64
                out = tf.image.resize_images(out, [75, 100], tf.image.ResizeMethod.BILINEAR)
                # 75x100x64
                out = tf.concat([out, concat1], 3)
                # 75x100x(64+64)

            with tf.variable_scope("conv13"):
                # 75x100x(64+64)
                out = tf.layers.conv2d(out, 64, [1, 1], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)

            with tf.variable_scope("conv14"):
                # 75x100x64
                out = tf.layers.conv2d(out, 32, [3, 3], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)

            with tf.variable_scope("conv15"):
                # 75x100x32
                out = tf.layers.conv2d(out, 32, [3, 3], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)

            with tf.variable_scope("concat5"):
                # 75x100x32
                out = tf.image.resize_images(out, [150, 200], tf.image.ResizeMethod.BILINEAR)
                # 150x200x32
                out = tf.concat([out, before_maxpool1], 3)
                # 150x200x(32+32)

            with tf.variable_scope("conv16"):
                # 150x200x(32+32)
                out = tf.layers.conv2d(out, 16, [1, 1], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)

            with tf.variable_scope("conv17"):
                # 150x200x16
                out = tf.layers.conv2d(out, 16, [3, 3], strides=[1, 1], padding="same")
                out = tf.layers.batch_normalization(out)
                out = tf.nn.relu(out)
                out = tf.nn.dropout(out, keep_prob=self._keep_prob)

            with tf.variable_scope("conv18"):
                # 150x200x16
                out = tf.layers.conv2d(out, 1, [3, 3], strides=[1, 1], padding="same")
                # out = tf.layers.batch_normalization(out)
                logits = out
                out = tf.maximum(tf.minimum(out, 1.0), 0.0)
                # 150x200x1

        return out, logits