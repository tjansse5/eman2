#ifndef eman__transform_h__
#define eman__transform_h__ 1

#include <gsl/gsl_linalg.h>
#include <string>
#include <vector>
#include "geometry.h"

using std::vector;
using std::string;

namespace EMAN {

    class Vec3f {
    public:
	Vec3f() {}
	Vec3f(float x, float y, float z) { vec[0] = x; vec[1] = y; vec[2] = z; }
	Vec3f(const float v[3]) { vec[0] = v[0]; vec[1] = v[1]; vec[2] = v[2]; }
	virtual ~Vec3f() {}
	
	float normalize();
	float dot(const Vec3f& v) { return (vec[0] * v[0] + vec[1] * v[1] + vec[2] * v[2]); }	
	
	float length() const;
	void negate() {  vec[0] = -vec[0]; vec[1] = -vec[1]; vec[2] = -vec[2]; }
	
	void get_value(float* v) { v[0] = vec[0]; v[1] = vec[1]; v[2] = vec[2]; }
	void get_value(float &x, float &y, float &z) { x = vec[0]; y = vec[1]; z = vec[2]; }

	void set_value(const float v[3]) { vec[0] = v[0]; vec[1] = v[1]; vec[2] = v[2]; }
	void set_value(float x, float y, float z) { vec[0] = x; vec[1] = y; vec[2] = z; }

	float operator[](int i) const { return vec[i]; }
	float& operator[](int i) { return vec[i]; }
	
	Vec3f& operator += (const Vec3f& v) { vec[0] += v[0]; vec[1] += v[1]; vec[2] += v[2]; return *this; }
	Vec3f& operator -= (const Vec3f& v) { vec[0] -= v[0]; vec[1] -= v[1]; vec[2] -= v[2]; return *this; }

	Vec3f& operator *= (float d) { vec[0] *= d; vec[1] *= d; vec[2] *= d; return *this; }
	Vec3f& operator /= (float d) { if (d != 0) { vec[0] /= d; vec[1] /= d; vec[2] /= d; } return *this; }

	friend Vec3f operator+(const Vec3f& v1, const Vec3f& v2);
	friend Vec3f operator-(const Vec3f& v1, const Vec3f& v2);

	friend Vec3f operator * (float d, const Vec3f v);
	friend Vec3f operator / (float d, const Vec3f v);
	
	friend Vec3f operator * (const Vec3f v, float d);
	friend Vec3f operator / (const Vec3f v, float d);
	
	friend bool operator==(const Vec3f& v1, const Vec3f& v2);
	friend bool operator!=(const Vec3f& v1, const Vec3f& v2);
	
    private:
	float vec[3];
    };

    
    class  Matrix3f {
    public:
	Matrix3f();
	Matrix3f(float m[]);
	virtual ~Matrix3f();
	
	Matrix3f& mult_right(const Matrix3f& m);
	Matrix3f& mult_left(const Matrix3f& m);
	
	void make_identity();
	
	void set_value(float m[]);
	void set_element(int i, int j, float v);
	
	void get_value(float m[]) const;
	float get_element(int i, int j) const;
	
	Matrix3f& inverse();
	Matrix3f create_inverse();

	Matrix3f& operator+=(float f);
	Matrix3f& operator-=(float f);
	Matrix3f& operator*=(float f);
	Matrix3f& operator/=(float f);
	
	Matrix3f& operator+=(const Matrix3f& m);
	Matrix3f& operator-=(const Matrix3f& m);
	Matrix3f& operator*=(const Matrix3f& m);
	Matrix3f& operator/=(const Matrix3f& m);

	double* operator[] (int i);
	const double* operator[] (int i) const;
	
	friend Matrix3f operator+(float f, const Matrix3f& m2);
	friend Matrix3f operator-(float f, const Matrix3f& m2);
	friend Matrix3f operator*(float f, const Matrix3f& m2);
	friend Matrix3f operator/(float f, const Matrix3f& m2);
	
	friend Matrix3f operator+(const Matrix3f& m1, float f);
	friend Matrix3f operator-(const Matrix3f& m1, float f);
	friend Matrix3f operator*(const Matrix3f& m1, float f);
	friend Matrix3f operator/(const Matrix3f& m1, float f);

	friend Matrix3f operator+(const Matrix3f& m1, const Matrix3f& m2);
	friend Matrix3f operator-(const Matrix3f& m1, const Matrix3f& m2);
	friend Matrix3f operator*(const Matrix3f& m1, const Matrix3f& m2);
	friend Matrix3f operator/(const Matrix3f& m1, const Matrix3f& m2);

	friend bool operator==(const Matrix3f& m1, const Matrix3f& m2);
	friend bool operator!=(const Matrix3f& m1, const Matrix3f& m2);
	
    private:
	Matrix3f(gsl_matrix* m);
	gsl_matrix* get_gsl_matrix() const;
	
	gsl_matrix* matrix;
    };

    
    class  Matrix4f {
    public:
	Matrix4f();
	Matrix4f(float m[]);
	virtual ~Matrix4f();
	
	Matrix4f& mult_right(const Matrix4f& m);
	Matrix4f& mult_left(const Matrix4f& m);
	
	void make_identity();
	
	void set_value(float m[]);
	void set_element(int i, int j, float v);
	
	void get_value(float m[]) const;
	float get_element(int i, int j) const;
	
	Matrix4f& inverse();
	Matrix4f create_inverse();

	Matrix4f& operator+=(float f);
	Matrix4f& operator-=(float f);
	Matrix4f& operator*=(float f);
	Matrix4f& operator/=(float f);
	
	Matrix4f& operator+=(const Matrix4f& m);
	Matrix4f& operator-=(const Matrix4f& m);
	Matrix4f& operator*=(const Matrix4f& m);
	Matrix4f& operator/=(const Matrix4f& m);
	
	double* operator[] (int i);
	const double* operator[] (int i) const;

	friend Matrix4f operator+(float f, const Matrix4f& m2);
	friend Matrix4f operator-(float f, const Matrix4f& m2);
	friend Matrix4f operator*(float f, const Matrix4f& m2);
	friend Matrix4f operator/(float f, const Matrix4f& m2);
	
	friend Matrix4f operator+(const Matrix4f& m1, float f);
	friend Matrix4f operator-(const Matrix4f& m1, float f);
	friend Matrix4f operator*(const Matrix4f& m1, float f);
	friend Matrix4f operator/(const Matrix4f& m1, float f);

	friend Matrix4f operator+(const Matrix4f& m1, const Matrix4f& m2);
	friend Matrix4f operator-(const Matrix4f& m1, const Matrix4f& m2);
	friend Matrix4f operator*(const Matrix4f& m1, const Matrix4f& m2);
	friend Matrix4f operator/(const Matrix4f& m1, const Matrix4f& m2);

	friend bool operator==(const Matrix4f& m1, const Matrix4f& m2);
	friend bool operator!=(const Matrix4f& m1, const Matrix4f& m2);
	
    private:
	Matrix4f(gsl_matrix* m);
	gsl_matrix* get_gsl_matrix() const;
	
	gsl_matrix* matrix;
    };
    

    class Rotation {
    public:
	enum Type { EMAN, IMAGIC, SPIN, QUAT, MATRIX, SGIROT, SPIDER, MRC };
    public:
	Rotation() {}
	Rotation(float a1, float a2, float a3, Type type);
	Rotation(float e1, float e2, float e3, float e0, Type type);
	Rotation(const Matrix3f& m);
	
	~Rotation();

	void inverse();
	Rotation create_inverse();
	
	float diff(Rotation* euler1, bool no_phi = true);
	void rotate_from_left(Rotation left_euler);
	void rotate_from_left(float alt, float az, float phi);

	void set_sym(string symname);
	int get_max_nsym() const;
	Rotation get_sym(int sym_index);

	void set_angle(float a1, float a2, float a3, Type type);
	void set_angle(float e1, float e2, float e3, float e0, Type type);
	void set_angle(const Matrix3f& m); 
	void set_type(Type type);
	
	bool is_valid() const;
	
	float eman_alt() const;
	float eman_az() const;
	float eman_phi() const;
	
	float mrc_theta() const;
	float mrc_phi() const;
	float mrc_omega() const;
    
	float imagic_alpha() const;
	float imagic_beta() const;
	float imagic_gamma() const;

	float spider_phi() const;
	float spider_theta() const;
	float spider_gamma() const;
    
	float spin_q() const;      
	float spin_n1() const;
	float spin_n2() const;
	float spin_n3() const;

	float sgi_q() const;      
	float sgi_n1() const;
	float sgi_n2() const;
	float sgi_n3() const;

	float quat_e0() const;
	float quat_e1() const;
	float quat_e2() const;
	float quat_e3() const;
	
	void get_matrix(Matrix3f& m) const;
	
	Rotation& operator*(const Rotation& e);
	Rotation& operator/(const Rotation& e);

	friend Rotation operator*(const Rotation& e1, const Rotation& e2);
	friend Rotation operator/(const Rotation& e1, const Rotation& e2);
	
	friend bool operator==(const Rotation& e1, const Rotation& e2);
	friend bool operator!=(const Rotation& e1, const Rotation& e2);

    private:
	Matrix3f matrix;
	Type type;
	string symname;
    };
    /*
      Euler angles have the disadvantage of being
      susceptible to "Gimbal lock" where attempts to rotate an
      object fail due to the order in which the rotations are performed.

      Quaternions are a solution to this problem. Instead of rotating an
      object through a series of successive rotations, a quaternion allows
      the programmer to rotate an object through a single arbitary rotation
      axis.

      Because the rotation axis is specifed as a unit direction vector,
      it may be calculated through vector mathematics or from spherical
      coordinates ie (longitude/latitude).

      Quaternions offer another advantage in that they be interpolated.
      This allows for smooth and predictable rotation effects.
    */
    
    class Quaternion {
    public:
	Quaternion();
	Quaternion(float radians, const Vec3f& axis);
	Quaternion(const Vec3f& axis, float radians);
	Quaternion(float e0, float e1, float e2, float e3);
	Quaternion(const Matrix4f& m);
	~Quaternion();

	float norm() const;
	Quaternion conj() const;
	float abs() const;
	
	void normalize();
	Quaternion& inverse();
	Quaternion create_inverse() const;
	
	Vec3f apply(const Vec3f& axis) const;
	
	float to_axis_angle(Vec3f& axis) const;
	Rotation to_euler() const;
	Matrix4f to_matrix() const;

	float real() const;
	Vec3f unreal() const;

	vector<float> get_value() const;
	
	Quaternion& operator+=(const Quaternion& q);
	Quaternion& operator-=(const Quaternion& q);
	Quaternion& operator*=(const Quaternion& q);
	Quaternion& operator*=(float s);
	Quaternion& operator/=(const Quaternion& q);
	Quaternion& operator/=(float s);
	
	friend Quaternion operator+(const Quaternion& q1, const Quaternion& q2);
	friend Quaternion operator-(const Quaternion& q1, const Quaternion& q2);

	friend Quaternion operator*(const Quaternion& q1, const Quaternion& q2);
	friend Quaternion operator*(const Quaternion& q, float s);
	friend Quaternion operator*(float s, const Quaternion& q);
	friend Quaternion operator/(const Quaternion& q1, const Quaternion& q2);

	friend bool operator==(const Quaternion& q1, const Quaternion& q2);
	friend bool operator!=(const Quaternion& q1, const Quaternion& q2);
	
    private:
	float e0;
	float e1;
	float e2;
	float e3;		
    };

    class Transform {
    public:
	enum TransformType {
	    ROTATION = 1 << 1,
	    TRANSLATION = 1 << 2,
	    SCALE = 1 << 3,
	    UNIFORM_SCALE = 1 << 4,
	    IDENTITY = 1 << 5,
	    TRANSFORM = 1 << 6
	};
	
	
    public:
	Transform(); // create an identity matrix
	Transform(const Matrix4f& m);
	Transform(float m[]);

	// Constructs and initializes a transform from the rotation
	// matrix, translation, and scale values. The scale is applied
	// only to the rotational component of the matrix (upper 3x3)
	// and not to the translational component of the matrix.
	Transform(const Matrix3f& m1, const Vec3f& t1, float s);
	
	virtual ~Transform();

	void set(const Rotation& r);
	void set(const Matrix3f& m);
	void set(float sx, float sy, float sz);
	void set(const Vec3f& s);

	void get_pre_translation() const;
	void get_post_translation() const;
	
	void concatenate(const Transform& t);      // [this] = [this] x [t]
	void pre_concatenate(const Transform& t);  // [this] = [t] x [this]
	
	void inverse();
	void transpose();
	void normalize();  
	
	void set_matrix(const Matrix4f& m);
	void get_matrix(Matrix4f& m);

	// Concatenates this transform with a translation transformation.
	void translate(float x, float y, float z);
	void translate(const Vec3f& v);
	
	Vec3f get_translation() const;

	// Concatenates this transform with a rotation transformation.
	void rotate(const Rotation& r);
	void rotate(const Matrix3f& m);
	//void rotate(const AxisAngle& a);

	// pre-translate, rotate, post-translate
	void rotate(const Rotation& r, const Vec3f& t);
	
	
	// Concatenates this transform with a scaling transformation.
	void scale(float sx, float sy, float sz);
	void scale(const Vec3f& scales);

	// pre-translate, rotate, scale on post-translate
	void rotate_scale(const Rotation& r, const Vec3f& t, float s);
	
	
	void get_rotation(Rotation& r) const;
	void get_rotation(Matrix3f& m);
	
	Vec3f get_scale() const;

	void set_center(float x, float y, float z);
	void set_center(const Vec3f& new_center);
	Vec3f get_center() const;

	Point<float> transform(const Point<float>& point_in);
	Vec3f transform(const Vec3f& vec_in);
	
	Point<float> back_transform(const Point<float>& point_out);
	Vec3f back_transform(const Vec3f& vec_out);
	
	
	int get_type() const;

	// add other combinations of operators
	Transform& operator+=(const Transform& t);
	friend Transform operator+(const Transform& t1, const Transform& t2);
	
	Transform& operator-=(const Transform& t);
	friend Transform operator-(const Transform& t1, const Transform& t2);

	Transform& operator*=(const Transform& t);
	Transform& operator*=(float scalar);

	friend Transform operator*(const Transform& t1, const Transform& t2);
	friend Transform operator*(const Transform& t, float s);
	friend Transform operator*(float s, const Transform& t);

	
	Transform& operator/=(const Transform& t);
	friend Transform operator/(const Transform& t1, const Transform& t2);
	friend Transform operator/(const Transform& t, float s);
	friend Transform operator/(float s, const Transform& t);
	
	
    private:
	Vec3f translation;
	Rotation rotation;
	Vec3f scale_factor;	// non-uniform scale
	Vec3f center;
    };


    

}


#endif
