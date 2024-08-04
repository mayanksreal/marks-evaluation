def build_model():
    from tensorflow.keras.models import load_model # type: ignore #ignore

    try:
        model = load_model("models/model.keras")

    except Exception:

        from tensorflow import keras
        from keras.models import Sequential # type: ignore
        from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input # type: ignore
        from keras.datasets import mnist # type: ignore
        from tensorflow.keras.preprocessing import image # type: ignore
        from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore
        from os import makedirs

        # Building model
        model = Sequential()
        model.add(Input(shape=(28,28,1)))

        # Convolutional layers
        model.add(Conv2D(32, (3,3), activation='relu'))
        model.add(MaxPooling2D(2,2))

        model.add(Conv2D(64, (3,3), activation='relu'))
        model.add(MaxPooling2D(2,2))

        model.add(Flatten())

        #Fully Connected layers
        model.add(Dense(64, activation='relu'))
        model.add(Dense(10, activation='softmax'))

        #Compilation
        model.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])

        #importing dataset
        (x_train, y_train) , (x_test, y_test) = mnist.load_data()
        x_train, y_train = x_train.reshape(60000, 28,28,1) , y_train.reshape(60000, 1)
        x_test, y_test = x_test.reshape(10000, 28,28,1) , y_test.reshape(10000, 1)
        x_train, x_test = x_train/255.0 , x_test/255.0

        #training
        model.fit(x = x_train , y = y_train, validation_split = 0.2, epochs = 5)

        try:
            makedirs("models/")
        except Exception:
            pass
        finally:
            model.save("models/model.keras")

    return model
