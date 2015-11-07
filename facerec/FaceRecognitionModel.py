'''
FaceRecognitionModel.py

Class for computing and storing the learned face feature model.

'''

import numpy as np


class FaceRecognitionModel:

    def __init__(self, k_rank=0):
        '''
        Initializer for the face recognition model.

        Args (optional):
            k_rank (int): How many principal components to keep. A value of 0
                indicates that it should be full-rank. (Default 0)
        '''

        self.k_rank = k_rank
        self.is_fitted = False
        self.trn_mean = 0


    def normalize(self, faces):
        '''
        Centers data to zero-mean.

        Args:
            faces (numpy.ndarray): Data to center.
        Returns:
            numpy.ndarray, the normalized data.
        '''

        out = np.array(faces, copy=True, dtype='float')

        mean = np.mean(out, axis=1)
        for x in out.T:
            x -= mean
        return out, mean


    def fit(self, faces):
        '''
        Fits a data matrix of faces to the model and learns features in the
        optimal subspace.

        Args:
            faces (numpy.ndarray): Data matrix of face vectors.
        '''

        faces, self.trn_mean = self.normalize(faces)

        # Perform SVD to get eigenvectors
        U,S,V = np.linalg.svd(faces, full_matrices=False)

        # Store top-k eigenvectors as components
        if self.k_rank != 0:
            self.components = U[0:self.k_rank]
        else:
            self.components = U

        self.is_fitted = True


    def transform(self, face):
        '''
        Transforms a set of faces by projecting it into the optimal subspace
        learned by PCA. Can be either a single face instance or multiple.

        Args:
            face (numpy.ndarray): Data matrix of face vectors.
        Returns:
            numpy.ndarray, the transformed matrix if the model has been fitted.
                None otherwise.
        '''

        if self.is_fitted:
            return self.components.T.dot(face-self.trn_mean)
        else:
            return None


# Command-Line Invocation

if __name__ == '__main__':
    pass

