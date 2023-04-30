const mongoose = require("mongoose");
const router = require("express").Router();
const { validateLead } = require("../models/lead");
const { User } = require("../models/user");

// GET request to retrieve all leads for a user
router.get("/:userId/leads", async (req, res) => {
  try {
    const user = await User.findById(req.params.userId);
    if (!user) {
      return res.status(404).send({ message: "User not found" });
    }
    res.status(200).send({
      data: user.leads,
      message: "Leads retrieved successfully",
    });
  } catch (error) {
    res.status(500).send({ message: "Internal Server Error" });
  }
});

// POST request to add a new lead for a user
router.post("/:userId/leads", async (req, res) => {
  try {
    const { error } = validateLead(req.body);
    if (error) {
      return res.status(400).send({ message: error.details[0].message });
    }

    const user = await User.findById(req.params.userId);
    if (!user) {
      return res.status(404).send({ message: "User not found" });
    }

    const lead = {
      _id: new mongoose.Types.ObjectId(),
      name: req.body.name,
      email: req.body.email,
      phone: req.body.phone,
    };

    user.leads.push(lead);
    await user.save();

    res.status(201).send({
      data: lead,
      message: "Lead added successfully",
    });
  } catch (error) {
    res.status(500).send({ message: "Internal Server Error" });
  }
});

// PUT request to update an existing lead for a user
router.put("/:userId/leads/:leadId", async (req, res) => {
  try {
    const { error } = validateLead(req.body);
    if (error) {
      return res.status(400).send({ message: error.details[0].message });
    }

    const user = await User.findById(req.params.userId);
    if (!user) {
      return res.status(404).send({ message: "User not found" });
    }

    const lead = user.leads.id(req.params.leadId);
    if (!lead) {
      return res.status(404).send({ message: "Lead not found" });
    }

    lead.name = req.body.name;
    lead.email = req.body.email;
    lead.phone = req.body.phone;

    await user.save();

    res.status(200).send({
      data: lead,
      message: "Lead updated successfully",
    });
  } catch (error) {
    res.status(500).send({ message: "Internal Server Error" });
  }
});

// DELETE request to delete an existing lead for a user
router.delete("/:userId/leads/:leadId", async (req, res) => {
  try {
    const user = await User.findById(req.params.userId);
    if (!user) {
      return res.status(404).send({ message: "User not found" });
    }

    const lead = user.leads.id(req.params.leadId);
    if (!lead) {
      return res.status(404).send({ message: "Lead not found" });
    }

    lead.remove();
    await user.save();

    res.status(200).send({
      data: lead,
      message: "Lead deleted successfully",
    });
  } catch (error) {
    res.status(500).send({ message: "Internal Server Error" });
  }
});

module.exports = router;
