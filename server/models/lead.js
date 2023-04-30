const mongoose = require("mongoose");
const Joi = require("joi");


const leadSchema = new mongoose.Schema({
    _id: mongoose.Schema.Types.ObjectId,
    name: { type: String, required: true },
    email: { type: String, required: true },
    phone: { type: String, required: true },
});

const Lead = mongoose.model("lead", leadSchema);

const validateLead = (data) => {
    const schema = Joi.object({
      name: Joi.string().required().label("Name"),
      email: Joi.string().email().required().label("Email"),
      phone: Joi.string().required().label("Phone"),
    });
    return schema.validate(data);
  };
  
  module.exports = { leadSchema, Lead, validateLead };